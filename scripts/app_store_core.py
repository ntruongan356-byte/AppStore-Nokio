#!/usr/bin/env python3
"""
Core App Store functionality for Google Colab
This module contains the main app store logic and utilities.
"""

import panel as pn
import os
import subprocess
import sys
import json
from pathlib import Path
import shutil
from typing import List, Dict, Any, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ColabAppStoreCore:
    """Core functionality for the Colab App Store"""
    
    def __init__(self, repo_path: str = "Ipynb-okio", base_path: str = "Pinokio-Apps"):
        """
        Initialize the app store core
        
        Args:
            repo_path: Path to the cloned repository
            base_path: Base path for Pinokio apps
        """
        self.repo_path = Path(repo_path)
        self.base_path = Path(base_path)
        self.apps: List[Dict[str, Any]] = []
        self.categories = {
            "1-Web-Development": [
                "1-Web-Development-Applications",
                "10-Web-Development-Applications",
            ],
            "2-Data-Science": [
                "2-Data-Science",
                "11-Data-Science-Applications",
            ],
            "3-Machine-Learning": [
                "3-Machine-Learning",
                "12-Machine-Learning-Applications",
            ],
            "4-Computer-Vision": [
                "4-Computer-Vision",
                "7-Computer-Vision-Applications",
            ],
            "5-Natural-Language-Processing": [
                "5-Natural-Language-Processing",
                "8-Natural-Language-Processing-Applications",
            ],
            "6-Generative-AI": [
                "6-Generative-AI",
                "9-Generative-AI-Applications",
            ]
        }
        
        logger.info(f"Initialized ColabAppStoreCore with repo_path={repo_path}, base_path={base_path}")
    
    def setup_environment(self) -> bool:
        """
        Setup the environment with required dependencies
        
        Returns:
            bool: True if setup successful, False otherwise
        """
        logger.info("Setting up environment...")
        
        try:
            # Install required packages
            required_packages = [
                "panel",
                "jupyter",
                "ipywidgets",
                "tqdm",
                "requests",
                "gitpython",
                "pathlib",
                "gradio",
                "ipython"
            ]
            
            for package in required_packages:
                try:
                    __import__(package)
                    logger.info(f"✅ {package} already installed")
                except ImportError:
                    logger.info(f"📦 Installing {package}...")
                    subprocess.run(
                        [sys.executable, "-m", "pip", "install", package],
                        capture_output=True,
                        timeout=300
                    )
            
            logger.info("✅ Environment setup complete!")
            return True
            
        except Exception as e:
            logger.error(f"❌ Environment setup failed: {e}")
            return False
    
    def clone_repository(self, repo_url: str) -> bool:
        """
        Clone the repository with all Pinokio apps
        
        Args:
            repo_url: URL of the repository to clone
            
        Returns:
            bool: True if clone successful, False otherwise
        """
        logger.info(f"Cloning repository: {repo_url}")
        
        try:
            # Remove existing repo if it exists
            if self.repo_path.exists():
                shutil.rmtree(self.repo_path)
            
            # Clone fresh repository
            result = subprocess.run(
                ["git", "clone", repo_url],
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode == 0:
                logger.info("✅ Repository cloned successfully!")
                return True
            else:
                logger.error(f"❌ Error cloning repository: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Exception cloning repository: {e}")
            return False
    
    def scan_repository_for_apps(self) -> List[Dict[str, Any]]:
        """
        Scan repository for apps and categorize them
        
        Returns:
            List of app dictionaries
        """
        logger.info("Scanning repository for apps...")
        apps = []
        
        if not self.repo_path.exists():
            logger.error("Repository path does not exist")
            return apps
        
        # Look for Python files and notebooks
        for file_path in self.repo_path.rglob("*"):
            if file_path.is_file() and file_path.suffix in ['.py', '.ipynb']:
                # Determine app type and category
                app_info = self.create_app_info(file_path)
                if app_info:
                    apps.append(app_info)
        
        logger.info(f"Found {len(apps)} apps")
        return sorted(apps, key=lambda x: x['name'])
    
    def create_app_info(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """
        Create app info from file path
        
        Args:
            file_path: Path to the app file
            
        Returns:
            App dictionary or None if creation failed
        """
        try:
            # Get app name from file or directory
            app_name = file_path.stem
            if file_path.parent.name != self.repo_path.name:
                app_name = file_path.parent.name
            
            # Determine app type
            app_type = self.detect_app_type(file_path)
            
            # Determine category based on app type and name
            category = self.determine_category(app_name, app_type)
            
            # Get folder size
            folder_size = self.get_folder_size(file_path.parent)
            
            app_info = {
                'name': app_name,
                'path': str(file_path.parent),
                'file_path': str(file_path),
                'type': app_type,
                'category': category,
                'size': folder_size,
                'has_requirements': self.has_requirements_file(file_path.parent),
                'has_readme': self.has_readme_file(file_path.parent)
            }
            
            return app_info
            
        except Exception as e:
            logger.error(f"Error creating app info for {file_path}: {e}")
            return None
    
    def detect_app_type(self, file_path: Path) -> str:
        """
        Detect app type based on file structure
        
        Args:
            file_path: Path to the app file
            
        Returns:
            String representing app type
        """
        file_name = file_path.name.lower()
        
        # Check for common app indicators
        app_indicators = {
            'streamlit': ['streamlit', 'app.py', 'streamlit_app.py'],
            'gradio': ['gradio', 'app.py', 'gradio_app.py'],
            'flask': ['flask', 'app.py', 'main.py', 'wsgi.py'],
            'fastapi': ['fastapi', 'main.py', 'app.py'],
            'jupyter': ['.ipynb'],
            'panel': ['panel', 'app.py', 'panel_app.py'],
            'dash': ['dash', 'app.py', 'index.py'],
            'plotly': ['plotly', 'app.py'],
            'python': ['main.py', 'run.py', 'app.py']
        }
        
        for app_type, indicators in app_indicators.items():
            for indicator in indicators:
                if indicator in file_name or indicator == file_path.suffix:
                    return app_type
        
        return 'unknown'
    
    def determine_category(self, app_name: str, app_type: str) -> str:
        """
        Determine category based on app name and type
        
        Args:
            app_name: Name of the app
            app_type: Type of the app
            
        Returns:
            String representing category
        """
        app_name_lower = app_name.lower()
        
        # Web development indicators
        web_dev_keywords = ['web', 'site', 'html', 'css', 'js', 'javascript', 'react', 'vue', 'angular', 'flask', 'fastapi', 'django']
        
        # Data science indicators
        data_science_keywords = ['data', 'analytics', 'visualization', 'pandas', 'numpy', 'matplotlib', 'seaborn', 'plotly', 'tableau']
        
        # Machine learning indicators
        ml_keywords = ['ml', 'machine', 'learning', 'train', 'model', 'tensorflow', 'pytorch', 'sklearn', 'xgboost', 'lightgbm']
        
        # Computer vision indicators
        cv_keywords = ['cv', 'vision', 'image', 'video', 'object', 'detection', 'segmentation', 'yolo', 'mask', 'rcnn']
        
        # NLP indicators
        nlp_keywords = ['nlp', 'text', 'language', 'sentence', 'word', 'token', 'bert', 'gpt', 'transformer', 'spacy']
        
        # GenAI indicators
        genai_keywords = ['genai', 'generative', 'ai', 'llm', 'diffusion', 'stable', 'midjourney', 'dalle', 'chatgpt']
        
        # Check keywords in order of priority
        if any(keyword in app_name_lower for keyword in web_dev_keywords):
            return '1-Web-Development'
        elif any(keyword in app_name_lower for keyword in data_science_keywords):
            return '2-Data-Science'
        elif any(keyword in app_name_lower for keyword in ml_keywords):
            return '3-Machine-Learning'
        elif any(keyword in app_name_lower for keyword in cv_keywords):
            return '4-Computer-Vision'
        elif any(keyword in app_name_lower for keyword in nlp_keywords):
            return '5-Natural-Language-Processing'
        elif any(keyword in app_name_lower for keyword in genai_keywords):
            return '6-Generative-AI'
        else:
            # Default category based on app type
            type_to_category = {
                'streamlit': '1-Web-Development',
                'gradio': '1-Web-Development',
                'flask': '1-Web-Development',
                'fastapi': '1-Web-Development',
                'jupyter': '2-Data-Science',
                'panel': '2-Data-Science',
                'dash': '2-Data-Science',
                'plotly': '2-Data-Science',
                'python': '3-Machine-Learning'
            }
            return type_to_category.get(app_type, '3-Machine-Learning')
    
    def has_requirements_file(self, folder_path: Path) -> bool:
        """
        Check if the folder has a requirements file
        
        Args:
            folder_path: Path to the folder
            
        Returns:
            bool: True if requirements file exists
        """
        req_files = ['requirements.txt', 'environment.yml', 'pyproject.toml', 'setup.py']
        return any((folder_path / req_file).exists() for req_file in req_files)
    
    def has_readme_file(self, folder_path: Path) -> bool:
        """
        Check if the folder has a README file
        
        Args:
            folder_path: Path to the folder
            
        Returns:
            bool: True if README file exists
        """
        readme_files = ['README.md', 'README.rst', 'README.txt', 'readme.md']
        return any((folder_path / readme_file).exists() for readme_file in readme_files)
    
    def get_folder_size(self, folder_path: Path) -> int:
        """
        Get the size of the folder
        
        Args:
            folder_path: Path to the folder
            
        Returns:
            int: Size in bytes
        """
        try:
            return sum(f.stat().st_size for f in folder_path.rglob('*') if f.is_file())
        except:
            return 0
    
    def format_size(self, size_bytes: int) -> str:
        """
        Format size in human readable format
        
        Args:
            size_bytes: Size in bytes
            
        Returns:
            String representing formatted size
        """
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"
    
    def organize_apps_into_categories(self) -> bool:
        """
        Organize apps into their respective category folders
        
        Returns:
            bool: True if organization successful
        """
        logger.info("Organizing apps into categories...")
        
        try:
            # Create symlinks or copy apps to category folders
            for category, subcategories in self.categories.items():
                category_path = self.base_path / category
                
                # Get apps for this category
                category_apps = [app for app in self.apps if app.get('category') == category]
                
                for app in category_apps:
                    app_name = app.get('name')
                    app_path = Path(app.get('path'))
                    
                    # Create symlink in category folder
                    symlink_path = category_path / app_name
                    
                    try:
                        if symlink_path.exists():
                            shutil.rmtree(symlink_path)
                        
                        # Create symlink
                        symlink_path.symlink_to(app_path, target_is_directory=True)
                        
                    except Exception as e:
                        # If symlink fails, copy the folder
                        try:
                            shutil.copytree(app_path, symlink_path)
                        except Exception as copy_error:
                            logger.error(f"Error copying {app_name}: {copy_error}")
            
            logger.info("✅ Apps organized successfully!")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error organizing apps: {e}")
            return False
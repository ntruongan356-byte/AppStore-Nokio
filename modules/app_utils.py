"""
App Utilities Module
This module contains utility functions for app management.
"""

import os
import subprocess
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


def detect_app_type(file_path: Path) -> str:
    """
    Detect app type based on file structure.
    
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


def determine_category(app_name: str, app_type: str) -> str:
    """
    Determine category based on app name and type.
    
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


def has_requirements_file(folder_path: Path) -> bool:
    """
    Check if the folder has a requirements file.
    
    Args:
        folder_path: Path to the folder
        
    Returns:
        bool: True if requirements file exists
    """
    req_files = ['requirements.txt', 'environment.yml', 'pyproject.toml', 'setup.py']
    return any((folder_path / req_file).exists() for req_file in req_files)


def has_readme_file(folder_path: Path) -> bool:
    """
    Check if the folder has a README file.
    
    Args:
        folder_path: Path to the folder
        
    Returns:
        bool: True if README file exists
    """
    readme_files = ['README.md', 'README.rst', 'README.txt', 'readme.md']
    return any((folder_path / readme_file).exists() for readme_file in readme_files)


def get_folder_size(folder_path: Path) -> int:
    """
    Get the size of the folder.
    
    Args:
        folder_path: Path to the folder
        
    Returns:
        int: Size in bytes
    """
    try:
        return sum(f.stat().st_size for f in folder_path.rglob('*') if f.is_file())
    except:
        return 0


def format_size(size_bytes: int) -> str:
    """
    Format size in human readable format.
    
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


def get_app_instructions(app_type: str, app_path: Path) -> str:
    """
    Get instructions for running different types of apps.
    
    Args:
        app_type: Type of the app
        app_path: Path to the app
        
    Returns:
        String containing instructions
    """
    
    if app_type == 'streamlit':
        return get_streamlit_instructions()
    elif app_type == 'gradio':
        return get_gradio_instructions()
    elif app_type == 'panel':
        return get_panel_instructions()
    elif app_type == 'jupyter':
        return get_jupyter_instructions()
    else:
        return get_python_instructions(app_path)


def get_streamlit_instructions() -> str:
    """Get instructions for running Streamlit apps."""
    return (
        "**Streamlit App Detected**\\n\\n" +
        "To run this Streamlit app in Google Colab, use the following commands:\\n\\n" +
        "```python\\n" +
        "# Install ngrok for tunneling\\n" +
        "!pip install streamlit pyngrok\\n\\n" +
        "# Set up ngrok tunnel\\n" +
        "from pyngrok import ngrok\\n" +
        "ngrok.set_auth_token(\"YOUR_NGROK_AUTH_TOKEN\")\\n" +
        "public_url = ngrok.connect(8501)\\n" +
        "print(f\"Streamlit app will be available at: {public_url}\")\\n\\n" +
        "# Run Streamlit in background\\n" +
        "!nohup streamlit run app.py --server.port 8501 &\\n" +
        "```\\n"
    )


def get_gradio_instructions() -> str:
    """Get instructions for running Gradio apps."""
    return (
        "**Gradio App Detected**\\n\\n" +
        "To run this Gradio app in Google Colab, use the following commands:\\n\\n" +
        "```python\\n" +
        "# Install dependencies if needed\\n" +
        "!pip install gradio\\n\\n" +
        "# Run the app (it will create a shareable link automatically)\\n" +
        "import gradio as gr\\n" +
        "# Import and run your gradio app here\\n" +
        "# Or use: !python app.py\\n" +
        "```\\n"
    )


def get_panel_instructions() -> str:
    """Get instructions for running Panel apps."""
    return (
        "**Panel App Detected**\\n\\n" +
        "To run this Panel app in Google Colab, use the following commands:\\n\\n" +
        "```python\\n" +
        "# Install panel if needed\\n" +
        "!pip install panel\\n\\n" +
        "# Import and run your panel app\\n" +
        "import panel as pn\\n" +
        "pn.extension(comms='colab')\\n" +
        "# Import and run your panel app here\\n" +
        "```\\n"
    )


def get_jupyter_instructions() -> str:
    """Get instructions for running Jupyter notebooks."""
    return (
        "**Jupyter Notebook Detected**\\n\\n" +
        "To run this Jupyter notebook in Google Colab:\\n\\n" +
        "1. Open the notebook file directly\\n" +
        "2. Or use:\\n```python\\n" +
        "# List available notebooks\\n" +
        "!ls *.ipynb\\n\\n" +
        "# Run a specific notebook\\n" +
        "!jupyter nbconvert --to notebook --execute your_notebook.ipynb\\n" +
        "```\\n"
    )


def get_python_instructions(app_path: Path) -> str:
    """Get instructions for running Python apps."""
    instructions = (
        "**Python App Detected**\\n\\n" +
        "To run this Python app in Google Colab:\\n\\n" +
        f"```python\\n" +
        f"# Change to app directory\\n" +
        f"%cd {app_path}\\n\\n" +
        f"# Install dependencies if available\\n" +
        f"!pip install -r requirements.txt 2>/dev/null || echo \"No requirements.txt found\"\\n\\n" +
        f"# Run the app\\n" +
        f"!python main.py  # or app.py, depending on the main file\\n" +
        f"```\\n\\n" +
        f"**Main Python files found:**\\n"
    )
    
    # List Python files
    try:
        py_files = list(app_path.rglob('*.py'))
        for py_file in py_files[:10]:  # Show first 10 Python files
            instructions += f"- `{py_file.relative_to(app_path)}`\\n"
        
        if len(py_files) > 10:
            instructions += f"... and {len(py_files) - 10} more files\\n"
    except Exception as e:
        instructions += f"Error listing files: {e}\\n"
    
    return instructions


def install_app_dependencies(app_path: Path) -> str:
    """
    Install dependencies for the selected app.
    
    Args:
        app_path: Path to the app
        
    Returns:
        String containing installation results
    """
    try:
        # Find requirements file
        req_file = None
        for req_name in ['requirements.txt', 'environment.yml', 'pyproject.toml']:
            if (app_path / req_name).exists():
                req_file = app_path / req_name
                break
        
        if req_file:
            if req_file.name == 'requirements.txt':
                result = subprocess.run(
                    [sys.executable, '-m', 'pip', 'install', '-r', str(req_file)],
                    capture_output=True,
                    text=True,
                    timeout=300
                )
                output = f"```\\n{result.stdout}\\n```\\n"
                if result.stderr:
                    output += f"**Errors:**\\n```\\n{result.stderr}\\n```\\n"
                return output
            else:
                return f"Requirements file found: {req_file.name}\\nPlease install dependencies manually for this file type.\\n"
        else:
            return "No requirements file found.\\n"
            
    except Exception as e:
        return f"Error installing dependencies: {e}\\n"


def read_app_readme(app_path: Path) -> str:
    """
    Read the README file of the selected app.
    
    Args:
        app_path: Path to the app
        
    Returns:
        String containing README content
    """
    try:
        # Find README file
        readme_file = None
        for readme_name in ['README.md', 'README.rst', 'README.txt', 'readme.md']:
            if (app_path / readme_name).exists():
                readme_file = app_path / readme_name
                break
        
        if readme_file:
            with open(readme_file, 'r', encoding='utf-8') as f:
                readme_content = f.read()
            
            # Convert markdown to display format
            return f"```\\n{readme_content}\\n```"
        else:
            return "No README file found.\\n"
            
    except Exception as e:
        return f"Error reading README: {e}\\n"


def create_app_symlink(source_path: Path, target_path: Path) -> bool:
    """
    Create symlink from source to target.
    
    Args:
        source_path: Source path
        target_path: Target path
        
    Returns:
        bool: True if symlink created successfully
    """
    try:
        if target_path.exists():
            import shutil
            shutil.rmtree(target_path)
        
        target_path.symlink_to(source_path, target_is_directory=True)
        return True
        
    except Exception as e:
        logger.error(f"Error creating symlink: {e}")
        
        # Try to copy instead
        try:
            import shutil
            shutil.copytree(source_path, target_path)
            return True
        except Exception as copy_error:
            logger.error(f"Error copying folder: {copy_error}")
            return False


def organize_apps_into_categories(apps: List[Dict[str, Any]], base_path: Path, categories: Dict[str, List[str]]) -> bool:
    """
    Organize apps into their respective category folders.
    
    Args:
        apps: List of app dictionaries
        base_path: Base path for Pinokio apps
        categories: Dictionary of categories
        
    Returns:
        bool: True if organization successful
    """
    try:
        # Create symlinks or copy apps to category folders
        for category, subcategories in categories.items():
            category_path = base_path / category
            
            # Get apps for this category
            category_apps = [app for app in apps if app.get('category') == category]
            
            for app in category_apps:
                app_name = app.get('name')
                app_path = Path(app.get('path'))
                
                # Create symlink in category folder
                symlink_path = category_path / app_name
                
                if not create_app_symlink(app_path, symlink_path):
                    logger.error(f"Failed to organize app: {app_name}")
        
        return True
        
    except Exception as e:
        logger.error(f"Error organizing apps: {e}")
        return False


def scan_repository_for_apps(repo_path: Path) -> List[Dict[str, Any]]:
    """
    Scan repository for apps and categorize them.
    
    Args:
        repo_path: Path to the repository
        
    Returns:
        List of app dictionaries
    """
    apps = []
    
    if not repo_path.exists():
        logger.error("Repository path does not exist")
        return apps
    
    # Look for Python files and notebooks
    for file_path in repo_path.rglob("*"):
        if file_path.is_file() and file_path.suffix in ['.py', '.ipynb']:
            # Determine app type and category
            app_info = create_app_info_from_file(file_path)
            if app_info:
                apps.append(app_info)
    
    logger.info(f"Found {len(apps)} apps")
    return sorted(apps, key=lambda x: x['name'])


def create_app_info_from_file(file_path: Path) -> Optional[Dict[str, Any]]:
    """
    Create app info from file path.
    
    Args:
        file_path: Path to the app file
        
    Returns:
        App dictionary or None if creation failed
    """
    try:
        # Get app name from file or directory
        app_name = file_path.stem
        if file_path.parent.name != file_path.parent.name:
            app_name = file_path.parent.name
        
        # Determine app type
        app_type = detect_app_type(file_path)
        
        # Determine category based on app type and name
        category = determine_category(app_name, app_type)
        
        # Get folder size
        folder_size = get_folder_size(file_path.parent)
        
        app_info = {
            'name': app_name,
            'path': str(file_path.parent),
            'file_path': str(file_path),
            'type': app_type,
            'category': category,
            'size': folder_size,
            'has_requirements': has_requirements_file(file_path.parent),
            'has_readme': has_readme_file(file_path.parent)
        }
        
        return app_info
        
    except Exception as e:
        logger.error(f"Error creating app info for {file_path}: {e}")
        return None
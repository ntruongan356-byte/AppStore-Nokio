#!/usr/bin/env python3
"""
Gradio UI components for the Colab App Store
This module contains Gradio-based user interface with share=true functionality.
"""

import gradio as gr
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional
import logging

# Import core functionality
from .app_store_core import ColabAppStoreCore

logger = logging.getLogger(__name__)


class GradioAppStoreUI:
    """Gradio-based UI for the Colab App Store"""
    
    def __init__(self, core: ColabAppStoreCore):
        """
        Initialize the Gradio UI
        
        Args:
            core: Core app store functionality instance
        """
        self.core = core
        self.selected_app = None
        
    def create_interface(self):
        """Create Gradio interface with share=true"""
        
        # Define CSS styling
        custom_css = """
        .gradio-container {
            max-width: 1200px !important;
            margin: 0 auto !important;
        }
        
        .app-card {
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 16px;
            border: 1px solid #e0e0e0;
        }
        
        .app-card:hover {
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        
        .category-badge {
            background-color: #1976d2;
            color: white;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
        }
        
        .status-success {
            color: #4caf50;
        }
        
        .status-error {
            color: #f44336;
        }
        
        .status-warning {
            color: #ff9800;
        }
        """
        
        # Create interface components
        with gr.Blocks(css=custom_css) as demo:
            
            # Header
            gr.Markdown("# 🚀 Clean Colab App Store")
            gr.Markdown("### 📋 Instructions")
            gr.Markdown(
                "1. **Categorize Apps**: Click the button to scan and categorize all apps\\n" +
                "2. **Browse Apps**: Use filters to find specific apps\\n" +
                "3. **Run Apps**: Click 'Run App' to launch selected applications\\n" +
                "4. **Share Interface**: Use the share button to create a public link"
            )
            
            with gr.Row():
                
                # Left panel - Controls
                with gr.Column(scale=1):
                    
                    # Status display
                    self.status_display = gr.Markdown(
                        "### 📊 Status\\n\\n" +
                        "✅ Environment ready\\n" +
                        "⏳ Ready to categorize apps"
                    )
                    
                    # Action buttons
                    self.categorize_btn = gr.Button(
                        "📂 Categorize All Apps",
                        variant="primary"
                    )
                    
                    self.clone_btn = gr.Button(
                        "📥 Clone Apps to Categories",
                        variant="secondary",
                        interactive=False
                    )
                    
                    # Filters
                    gr.Markdown("### 🔍 Filters")
                    
                    self.search_box = gr.Textbox(
                        label="Search Apps",
                        placeholder="Type to filter apps..."
                    )
                    
                    self.category_filter = gr.CheckboxGroup(
                        label="Filter by Category",
                        choices=list(self.core.categories.keys()),
                        value=list(self.core.categories.keys())
                    )
                    
                    self.type_filter = gr.CheckboxGroup(
                        label="Filter by Type",
                        choices=[],
                        value=[]
                    )
                    
                    # App selector
                    self.app_selector = gr.Dropdown(
                        label="Select App",
                        choices=[],
                        value=None
                    )
                    
                    # Action buttons for selected app
                    self.install_deps_btn = gr.Button(
                        "📦 Install Dependencies",
                        variant="primary",
                        interactive=False
                    )
                    
                    self.run_app_btn = gr.Button(
                        "🚀 Run App",
                        variant="success",
                        interactive=False
                    )
                    
                    self.view_readme_btn = gr.Button(
                        "📖 View README",
                        variant="secondary",
                        interactive=False
                    )
                
                # Right panel - Display
                with gr.Column(scale=2):
                    
                    # App details
                    self.app_details = gr.Markdown(
                        "### 📋 App Details\\n\\n" +
                        "Select an app to view details"
                    )
                    
                    # Output area
                    self.output_area = gr.Markdown(
                        "### 📋 Output\\n\\n" +
                        "Ready to categorize apps..."
                    )
            
            # Bind events
            self.categorize_btn.click(
                self.categorize_apps,
                outputs=[self.status_display, self.category_filter, self.type_filter, 
                        self.app_selector, self.clone_btn, self.output_area]
            )
            
            self.clone_btn.click(
                self.clone_apps,
                outputs=[self.status_display, self.output_area]
            )
            
            self.search_box.change(
                self.update_filters,
                inputs=[self.search_box, self.category_filter, self.type_filter],
                outputs=[self.app_selector]
            )
            
            self.category_filter.change(
                self.update_filters,
                inputs=[self.search_box, self.category_filter, self.type_filter],
                outputs=[self.app_selector]
            )
            
            self.type_filter.change(
                self.update_filters,
                inputs=[self.search_box, self.category_filter, self.type_filter],
                outputs=[self.app_selector]
            )
            
            self.app_selector.change(
                self.on_app_selected,
                outputs=[self.app_details, self.install_deps_btn, self.view_readme_btn]
            )
            
            self.install_deps_btn.click(
                self.install_dependencies,
                outputs=[self.output_area]
            )
            
            self.run_app_btn.click(
                self.run_app,
                outputs=[self.output_area]
            )
            
            self.view_readme_btn.click(
                self.view_readme,
                outputs=[self.output_area]
            )
        
        return demo
    
    def categorize_apps(self):
        """Categorize all apps in the repository"""
        try:
            # Scan repository for apps
            self.core.apps = self.core.scan_repository_for_apps()
            
            # Update filter options
            app_types = list(set(app['type'] for app in self.core.apps))
            self.type_filter.choices = app_types
            
            # Update status
            status_text = (
                f"### 📊 Status\\n\\n" +
                f"✅ Environment ready\\n" +
                f"✅ Found {len(self.core.apps)} apps\\n" +
                f"✅ Categorized into {len(self.core.categories)} categories"
            )
            
            # Update app selector
            app_names = [app['name'] for app in self.core.apps]
            self.app_selector.choices = app_names
            
            # Enable clone button
            clone_interactive = len(self.core.apps) > 0
            
            # Create output text
            output_text = (
                f"### ✅ Categorization Complete!\\n\\n" +
                f"Found {len(self.core.apps)} apps across {len(self.core.categories)} categories.\\n\\n" +
                f"### 📊 Category Summary\\n\\n"
            )
            
            # Show category summary
            for category, subcategories in self.core.categories.items():
                category_count = len([app for app in self.core.apps if app.get('category') == category])
                output_text += f"**{category}**: {category_count} apps\\n"
            
            return status_text, list(self.core.categories.keys()), app_types, app_names, clone_interactive, output_text
            
        except Exception as e:
            error_text = f"### ❌ Error categorizing apps: {e}"
            return error_text, list(self.core.categories.keys()), [], [], False, error_text
    
    def clone_apps(self):
        """Clone apps to their respective category folders"""
        try:
            # Create symlinks or copy apps to category folders
            success = self.core.organize_apps_into_categories()
            
            if success:
                status_text = (
                    f"### 📊 Status\\n\\n" +
                    f"✅ Environment ready\\n" +
                    f"✅ Found {len(self.core.apps)} apps\\n" +
                    f"✅ Apps organized into categories"
                )
                
                # Create output text
                output_text = (
                    f"### ✅ Apps Cloned Successfully!\\n\\n" +
                    f"{len(self.core.apps)} apps organized into {len(self.core.categories)} categories.\\n\\n" +
                    f"### 📁 Category Structure\\n\\n"
                )
                
                # Show category structure
                for category in self.core.categories.keys():
                    category_path = Path(f"Pinokio-Apps/{category}")
                    if category_path.exists():
                        app_count = len(list(category_path.iterdir()))
                        output_text += f"**{category}**: {app_count} apps\\n"
                
                return status_text, output_text
            else:
                error_text = "### ❌ Error cloning apps"
                return error_text, error_text
                
        except Exception as e:
            error_text = f"### ❌ Error cloning apps: {e}"
            return error_text, error_text
    
    def update_filters(self, search_text, selected_categories, selected_types):
        """Update app selector based on filters"""
        try:
            filtered_apps = self.core.apps
            
            # Apply search filter
            if search_text:
                search_term = search_text.lower()
                filtered_apps = [app for app in filtered_apps 
                               if search_term in app['name'].lower()]
            
            # Apply category filter
            if selected_categories:
                filtered_apps = [app for app in filtered_apps 
                               if app['category'] in selected_categories]
            
            # Apply type filter
            if selected_types:
                filtered_apps = [app for app in filtered_apps 
                               if app['type'] in selected_types]
            
            # Update app selector
            app_names = [app['name'] for app in filtered_apps]
            
            return gr.Dropdown(choices=app_names, value=app_names[0] if app_names else None)
            
        except Exception as e:
            logger.error(f"Error updating filters: {e}")
            return gr.Dropdown(choices=[], value=None)
    
    def on_app_selected(self):
        """Handle app selection"""
        try:
            if not self.app_selector.value:
                return "### 📋 App Details\\n\\nSelect an app to view details", False, False
            
            # Get selected app
            self.selected_app = next((app for app in self.core.apps if app['name'] == self.app_selector.value), None)
            
            if not self.selected_app:
                return "### 📋 App Details\\n\\nApp not found", False, False
            
            # Create app details text
            app = self.selected_app
            details_text = (
                f"### {app['name']}\\n\\n" +
                f"**Type:** `{app['type']}`\\n" +
                f"**Category:** `{app['category']}`\\n" +
                f"**Path:** `{app['path']}`\\n" +
                f"**Size:** `{self.core.format_size(app['size'])}`\\n\\n" +
                f"**Features:**\\n" +
                f"- {'✅' if app['has_requirements'] else '❌'} Has requirements file\\n" +
                f"- {'✅' if app['has_readme'] else '❌'} Has README\\n\\n" +
                f"**Files:**\\n"
            )
            
            # List some key files
            try:
                files = list(Path(app['path']).rglob('*'))[:20]  # Limit to first 20 files
                for file in files:
                    if file.is_file():
                        details_text += f"- `{file.relative_to(app['path'])}`\\n"
            except Exception as e:
                details_text += f"Error listing files: {e}\\n"
            
            # Update button states
            install_interactive = app['has_requirements']
            readme_interactive = app['has_readme']
            
            return details_text, install_interactive, readme_interactive
            
        except Exception as e:
            error_text = f"### ❌ Error selecting app: {e}"
            return error_text, False, False
    
    def install_dependencies(self):
        """Install dependencies for the selected app"""
        try:
            if not self.selected_app:
                return "### ❌ No app selected"
            
            app = self.selected_app
            output_text = f"### 📦 Installing dependencies for {app['name']}...\\n\\n"
            
            # Find requirements file
            req_file = None
            for req_name in ['requirements.txt', 'environment.yml', 'pyproject.toml']:
                if (Path(app['path']) / req_name).exists():
                    req_file = Path(app['path']) / req_name
                    break
            
            if req_file:
                if req_file.name == 'requirements.txt':
                    result = subprocess.run(
                        [sys.executable, '-m', 'pip', 'install', '-r', str(req_file)],
                        capture_output=True,
                        text=True,
                        timeout=300
                    )
                    output_text += f"```\\n{result.stdout}\\n```\\n"
                    if result.stderr:
                        output_text += f"**Errors:**\\n```\\n{result.stderr}\\n```\\n"
                else:
                    output_text += f"Requirements file found: {req_file.name}\\n"
                    output_text += "Please install dependencies manually for this file type.\\n"
            else:
                output_text += "No requirements file found.\\n"
            
            return output_text
            
        except Exception as e:
            return f"### ❌ Error installing dependencies: {e}"
    
    def run_app(self):
        """Run the selected app"""
        try:
            if not self.selected_app:
                return "### ❌ No app selected"
            
            app = self.selected_app
            output_text = f"### 🚀 Running {app['name']}...\\n\\n"
            
            # Change to app directory
            os.chdir(app['path'])
            
            # Determine how to run the app based on its type
            if app['type'] == 'streamlit':
                output_text += self.get_streamlit_instructions(app)
            elif app['type'] == 'gradio':
                output_text += self.get_gradio_instructions(app)
            elif app['type'] == 'panel':
                output_text += self.get_panel_instructions(app)
            elif app['type'] == 'jupyter':
                output_text += self.get_jupyter_instructions(app)
            else:
                # Generic Python app
                output_text += self.get_python_instructions(app)
            
            return output_text
            
        except Exception as e:
            return f"### ❌ Error running app: {e}"
        finally:
            # Change back to original directory
            os.chdir('/content')
    
    def get_streamlit_instructions(self, app):
        """Get instructions for running Streamlit apps"""
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
    
    def get_gradio_instructions(self, app):
        """Get instructions for running Gradio apps"""
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
    
    def get_panel_instructions(self, app):
        """Get instructions for running Panel apps"""
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
    
    def get_jupyter_instructions(self, app):
        """Get instructions for running Jupyter notebooks"""
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
    
    def get_python_instructions(self, app):
        """Get instructions for running Python apps"""
        instructions = (
            "**Python App Detected**\\n\\n" +
            "To run this Python app in Google Colab:\\n\\n" +
            f"```python\\n" +
            f"# Change to app directory\\n" +
            f"%cd {app['path']}\\n\\n" +
            f"# Install dependencies if available\\n" +
            f"!pip install -r requirements.txt 2>/dev/null || echo \"No requirements.txt found\"\\n\\n" +
            f"# Run the app\\n" +
            f"!python main.py  # or app.py, depending on the main file\\n" +
            f"```\\n\\n" +
            f"**Main Python files found:**\\n"
        )
        
        # List Python files
        try:
            py_files = list(Path(app['path']).rglob('*.py'))
            for py_file in py_files[:10]:  # Show first 10 Python files
                instructions += f"- `{py_file.relative_to(app['path'])}`\\n"
            
            if len(py_files) > 10:
                instructions += f"... and {len(py_files) - 10} more files\\n"
        except Exception as e:
            instructions += f"Error listing files: {e}\\n"
        
        return instructions
    
    def view_readme(self):
        """View the README file of the selected app"""
        try:
            if not self.selected_app:
                return "### ❌ No app selected"
            
            app = self.selected_app
            output_text = f"### 📖 README for {app['name']}\\n\\n"
            
            # Find README file
            readme_file = None
            for readme_name in ['README.md', 'README.rst', 'README.txt', 'readme.md']:
                if (Path(app['path']) / readme_name).exists():
                    readme_file = Path(app['path']) / readme_name
                    break
            
            if readme_file:
                with open(readme_file, 'r', encoding='utf-8') as f:
                    readme_content = f.read()
                
                # Convert markdown to display format
                output_text += f"```\\n{readme_content}\\n```"
            else:
                output_text += "No README file found.\\n"
            
            return output_text
            
        except Exception as e:
            return f"### ❌ Error reading README: {e}"
    
    def launch(self, share=True):
        """Launch the Gradio interface"""
        try:
            # Create interface
            demo = self.create_interface()
            
            # Launch with share option
            if share:
                demo.launch(share=True)
            else:
                demo.launch()
                
        except Exception as e:
            logger.error(f"Error launching Gradio interface: {e}")
            raise
#!/usr/bin/env python3
"""
IPy Widgets UI components for the Colab App Store
This module contains IPython widget-based user interface.
"""

import ipywidgets as widgets
from IPython.display import display, HTML, Javascript
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional
import logging

# Import core functionality
from .app_store_core import ColabAppStoreCore

logger = logging.getLogger(__name__)


class IPyWidgetsAppStoreUI:
    """IPython widget-based UI for the Colab App Store"""
    
    def __init__(self, core: ColabAppStoreCore):
        """
        Initialize the IPyWidgets UI
        
        Args:
            core: Core app store functionality instance
        """
        self.core = core
        self.selected_app = None
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the IPyWidgets UI components"""
        
        # Create custom CSS
        custom_css = widgets.HTML(
            """
            <style>
            .widget-container {
                padding: 10px;
                margin: 5px 0;
                border: 1px solid #e0e0e0;
                border-radius: 5px;
            }
            
            .widget-header {
                font-weight: bold;
                color: #1976d2;
                margin-bottom: 10px;
            }
            
            .app-card {
                padding: 15px;
                margin: 10px 0;
                border: 1px solid #ddd;
                border-radius: 8px;
                background-color: #f9f9f9;
            }
            
            .app-card:hover {
                background-color: #f0f0f0;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            
            .category-badge {
                background-color: #1976d2;
                color: white;
                padding: 4px 8px;
                border-radius: 4px;
                font-size: 12px;
                margin: 2px;
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
            
            .btn-primary {
                background-color: #1976d2;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                cursor: pointer;
            }
            
            .btn-success {
                background-color: #4caf50;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                cursor: pointer;
            }
            
            .btn-secondary {
                background-color: #757575;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                cursor: pointer;
            }
            
            .output-area {
                max-height: 400px;
                overflow-y: auto;
                border: 1px solid #ddd;
                padding: 10px;
                border-radius: 4px;
                background-color: #fafafa;
            }
            </style>
            """
        )
        
        # Header
        header = widgets.HTML(
            """
            <div style="text-align: center; margin-bottom: 20px;">
                <h1>🚀 Clean Colab App Store</h1>
                <h3>📋 Instructions</h3>
                <p>1. <strong>Categorize Apps</strong>: Click the button to scan and categorize all apps</p>
                <p>2. <strong>Browse Apps</strong>: Use filters to find specific apps</p>
                <p>3. <strong>Run Apps</strong>: Click 'Run App' to launch selected applications</p>
            </div>
            """
        )
        
        # Status display
        self.status_display = widgets.HTML(
            """
            <div class="widget-container">
                <div class="widget-header">📊 Status</div>
                <div>✅ Environment ready</div>
                <div>⏳ Ready to categorize apps</div>
            </div>
            """
        )
        
        # Action buttons
        self.categorize_btn = widgets.Button(
            description="📂 Categorize All Apps",
            button_style='primary',
            layout=widgets.Layout(width='auto')
        )
        
        self.clone_btn = widgets.Button(
            description="📥 Clone Apps to Categories",
            button_style='info',
            layout=widgets.Layout(width='auto'),
            disabled=True
        )
        
        # Filters section
        filters_header = widgets.HTML("<div class='widget-header'>🔍 Filters</div>")
        
        self.search_box = widgets.Text(
            placeholder="Type to filter apps...",
            layout=widgets.Layout(width='100%')
        )
        
        self.category_filter = widgets.SelectionRangeSlider(
            options=list(self.core.categories.keys()),
            value=(list(self.core.categories.keys())[0], list(self.core.categories.keys())[-1]),
            description="Category Range",
            layout=widgets.Layout(width='100%')
        )
        
        self.type_filter = widgets.SelectMultiple(
            options=[],
            description="App Types",
            layout=widgets.Layout(width='100%')
        )
        
        # App selector
        self.app_selector = widgets.Dropdown(
            options=[],
            description="Select App",
            layout=widgets.Layout(width='100%')
        )
        
        # Action buttons for selected app
        self.install_deps_btn = widgets.Button(
            description="📦 Install Dependencies",
            button_style='primary',
            layout=widgets.Layout(width='auto'),
            disabled=True
        )
        
        self.run_app_btn = widgets.Button(
            description="🚀 Run App",
            button_style='success',
            layout=widgets.Layout(width='auto'),
            disabled=True
        )
        
        self.view_readme_btn = widgets.Button(
            description="📖 View README",
            button_style='secondary',
            layout=widgets.Layout(width='auto'),
            disabled=True
        )
        
        # App details display
        self.app_details = widgets.HTML(
            """
            <div class="widget-container">
                <div class="widget-header">📋 App Details</div>
                <div>Select an app to view details</div>
            </div>
            """
        )
        
        # Output area
        self.output_area = widgets.HTML(
            """
            <div class="output-area">
                <div class="widget-header">📋 Output</div>
                <div>Ready to categorize apps...</div>
            </div>
            """
        )
        
        # Bind events
        self.categorize_btn.on_click(self.categorize_apps)
        self.clone_btn.on_click(self.clone_apps)
        self.search_box.observe(self.on_search_changed, names='value')
        self.category_filter.observe(self.on_category_filter_changed, names='value')
        self.type_filter.observe(self.on_type_filter_changed, names='value')
        self.app_selector.observe(self.on_app_selected, names='value')
        self.install_deps_btn.on_click(self.install_dependencies)
        self.run_app_btn.on_click(self.run_app)
        self.view_readme_btn.on_click(self.view_readme)
        
        # Create layout
        self.create_layout()
    
    def create_layout(self):
        """Create the widget layout"""
        
        # Left panel
        left_panel = widgets.VBox([
            self.status_display,
            widgets.HTML("<br>"),
            self.categorize_btn,
            self.clone_btn,
            widgets.HTML("<br>"),
            filters_header,
            self.search_box,
            self.category_filter,
            self.type_filter,
            widgets.HTML("<br>"),
            self.app_selector,
            widgets.HTML("<br>"),
            self.install_deps_btn,
            self.run_app_btn,
            self.view_readme_btn
        ], layout=widgets.Layout(width='400px'))
        
        # Right panel
        right_panel = widgets.VBox([
            self.app_details,
            widgets.HTML("<br>"),
            self.output_area
        ], layout=widgets.Layout(width='auto'))
        
        # Main layout
        self.main_layout = widgets.HBox([left_panel, right_panel])
        
        # Display the layout
        display(widgets.HTML("<div style='margin: 20px;'>"))
        display(self.main_layout)
        display(widgets.HTML("</div>"))
    
    def categorize_apps(self, b):
        """Categorize all apps in the repository"""
        try:
            # Update status
            self.status_display.value = (
                "<div class='widget-container'>" +
                "<div class='widget-header'>📊 Status</div>" +
                "<div>✅ Environment ready</div>" +
                "<div>🔄 Categorizing apps...</div>" +
                "</div>"
            )
            
            # Scan repository for apps
            self.core.apps = self.core.scan_repository_for_apps()
            
            # Update filter options
            app_types = list(set(app['type'] for app in self.core.apps))
            self.type_filter.options = app_types
            
            # Update app selector
            app_names = [app['name'] for app in self.core.apps]
            self.app_selector.options = app_names
            
            # Enable clone button
            self.clone_btn.disabled = len(self.core.apps) == 0
            
            # Update status
            status_text = (
                f"<div class='widget-container'>" +
                f"<div class='widget-header'>📊 Status</div>" +
                f"<div>✅ Environment ready</div>" +
                f"<div>✅ Found {len(self.core.apps)} apps</div>" +
                f"<div>✅ Categorized into {len(self.core.categories)} categories</div>" +
                f"</div>"
            )
            
            self.status_display.value = status_text
            
            # Create output text
            output_text = (
                f"<div class='output-area'>" +
                f"<div class='widget-header'>✅ Categorization Complete!</div>" +
                f"<p>Found {len(self.core.apps)} apps across {len(self.core.categories)} categories.</p>" +
                f"<h4>📊 Category Summary</h4>" +
                f"<ul>"
            )
            
            # Show category summary
            for category, subcategories in self.core.categories.items():
                category_count = len([app for app in self.core.apps if app.get('category') == category])
                output_text += f"<li><strong>{category}</strong>: {category_count} apps</li>"
            
            output_text += f"</ul></div>"
            
            self.output_area.value = output_text
            
        except Exception as e:
            error_text = (
                f"<div class='output-area'>" +
                f"<div class='widget-header'>❌ Error</div>" +
                f"<p>Error categorizing apps: {e}</p>" +
                f"</div>"
            )
            
            self.output_area.value = error_text
    
    def clone_apps(self, b):
        """Clone apps to their respective category folders"""
        try:
            # Update status
            self.status_display.value = (
                "<div class='widget-container'>" +
                "<div class='widget-header'>📊 Status</div>" +
                "<div>✅ Environment ready</div>" +
                "<div>✅ Found {len(self.core.apps)} apps</div>" +
                "<div>🔄 Cloning apps...</div>" +
                "</div>"
            )
            
            # Create symlinks or copy apps to category folders
            success = self.core.organize_apps_into_categories()
            
            if success:
                # Update status
                status_text = (
                    f"<div class='widget-container'>" +
                    f"<div class='widget-header'>📊 Status</div>" +
                    f"<div>✅ Environment ready</div>" +
                    f"<div>✅ Found {len(self.core.apps)} apps</div>" +
                    f"<div>✅ Apps organized into categories</div>" +
                    f"</div>"
                )
                
                self.status_display.value = status_text
                
                # Create output text
                output_text = (
                    f"<div class='output-area'>" +
                    f"<div class='widget-header'>✅ Apps Cloned Successfully!</div>" +
                    f"<p>{len(self.core.apps)} apps organized into {len(self.core.categories)} categories.</p>" +
                    f"<h4>📁 Category Structure</h4>" +
                    f"<ul>"
                )
                
                # Show category structure
                for category in self.core.categories.keys():
                    category_path = Path(f"Pinokio-Apps/{category}")
                    if category_path.exists():
                        app_count = len(list(category_path.iterdir()))
                        output_text += f"<li><strong>{category}</strong>: {app_count} apps</li>"
                
                output_text += f"</ul></div>"
                
                self.output_area.value = output_text
            else:
                error_text = (
                    f"<div class='output-area'>" +
                    f"<div class='widget-header'>❌ Error</div>" +
                    f"<p>Error cloning apps</p>" +
                    f"</div>"
                )
                
                self.output_area.value = error_text
                
        except Exception as e:
            error_text = (
                f"<div class='output-area'>" +
                f"<div class='widget-header'>❌ Error</div>" +
                f"<p>Error cloning apps: {e}</p>" +
                f"</div>"
            )
            
            self.output_area.value = error_text
    
    def on_search_changed(self, change):
        """Handle search filter change"""
        self.update_app_selector()
    
    def on_category_filter_changed(self, change):
        """Handle category filter change"""
        self.update_app_selector()
    
    def on_type_filter_changed(self, change):
        """Handle type filter change"""
        self.update_app_selector()
    
    def update_app_selector(self):
        """Update the app selector options based on filters"""
        try:
            filtered_apps = self.core.apps
            
            # Apply search filter
            if self.search_box.value:
                search_term = self.search_box.value.lower()
                filtered_apps = [app for app in filtered_apps 
                               if search_term in app['name'].lower()]
            
            # Apply category filter
            if self.category_filter.value:
                selected_categories = list(range(
                    list(self.core.categories.keys()).index(self.category_filter.value[0]),
                    list(self.core.categories.keys()).index(self.category_filter.value[1]) + 1
                ))
                category_names = [list(self.core.categories.keys())[i] for i in selected_categories]
                filtered_apps = [app for app in filtered_apps 
                               if app['category'] in category_names]
            
            # Apply type filter
            if self.type_filter.value:
                filtered_apps = [app for app in filtered_apps 
                               if app['type'] in self.type_filter.value]
            
            # Update app selector
            self.app_selector.options = [app['name'] for app in filtered_apps]
            
            # Update selection if current selection is not in filtered list
            if self.app_selector.value and self.app_selector.value not in self.app_selector.options:
                self.app_selector.value = self.app_selector.options[0] if self.app_selector.options else None
            
        except Exception as e:
            logger.error(f"Error updating app selector: {e}")
    
    def on_app_selected(self, change):
        """Handle app selection"""
        try:
            if not self.app_selector.value:
                self.app_details.value = (
                    "<div class='widget-container'>" +
                    "<div class='widget-header'>📋 App Details</div>" +
                    "<div>Select an app to view details</div>" +
                    "</div>"
                )
                self.install_deps_btn.disabled = True
                self.view_readme_btn.disabled = True
                return
            
            # Get selected app
            self.selected_app = next((app for app in self.core.apps if app['name'] == self.app_selector.value), None)
            
            if not self.selected_app:
                self.app_details.value = (
                    "<div class='widget-container'>" +
                    "<div class='widget-header'>📋 App Details</div>" +
                    "<div>App not found</div>" +
                    "</div>"
                )
                self.install_deps_btn.disabled = True
                self.view_readme_btn.disabled = True
                return
            
            # Create app details text
            app = self.selected_app
            details_text = (
                f"<div class='app-card'>" +
                f"<h3>{app['name']}</h3>" +
                f"<p><strong>Type:</strong> <code>{app['type']}</code></p>" +
                f"<p><strong>Category:</strong> <code>{app['category']}</code></p>" +
                f"<p><strong>Path:</strong> <code>{app['path']}</code></p>" +
                f"<p><strong>Size:</strong> <code>{self.core.format_size(app['size'])}</code></p>" +
                f"<h4>Features:</h4>" +
                f"<ul>" +
                f"<li>{'✅' if app['has_requirements'] else '❌'} Has requirements file</li>" +
                f"<li>{'✅' if app['has_readme'] else '❌'} Has README</li>" +
                f"</ul>" +
                f"<h4>Files:</h4>" +
                f"<ul>"
            )
            
            # List some key files
            try:
                files = list(Path(app['path']).rglob('*'))[:20]  # Limit to first 20 files
                for file in files:
                    if file.is_file():
                        details_text += f"<li><code>{file.relative_to(app['path'])}</code></li>"
            except Exception as e:
                details_text += f"<li>Error listing files: {e}</li>"
            
            details_text += f"</ul></div>"
            
            self.app_details.value = details_text
            
            # Update button states
            self.install_deps_btn.disabled = not app['has_requirements']
            self.view_readme_btn.disabled = not app['has_readme']
            
        except Exception as e:
            error_text = (
                f"<div class='widget-container'>" +
                f"<div class='widget-header'>❌ Error</div>" +
                f"<p>Error selecting app: {e}</p>" +
                f"</div>"
            )
            
            self.app_details.value = error_text
            self.install_deps_btn.disabled = True
            self.view_readme_btn.disabled = True
    
    def install_dependencies(self, b):
        """Install dependencies for the selected app"""
        try:
            if not self.selected_app:
                self.output_area.value = (
                    "<div class='output-area'>" +
                    "<div class='widget-header'>❌ Error</div>" +
                    "<p>No app selected</p>" +
                    "</div>"
                )
                return
            
            app = self.selected_app
            output_text = f"<div class='output-area'><div class='widget-header'>📦 Installing dependencies for {app['name']}...</div>"
            
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
                    output_text += f"<pre>{result.stdout}</pre>"
                    if result.stderr:
                        output_text += f"<p><strong>Errors:</strong></p><pre>{result.stderr}</pre>"
                else:
                    output_text += f"<p>Requirements file found: {req_file.name}</p>"
                    output_text += "<p>Please install dependencies manually for this file type.</p>"
            else:
                output_text += "<p>No requirements file found.</p>"
            
            output_text += "</div>"
            self.output_area.value = output_text
            
        except Exception as e:
            error_text = (
                f"<div class='output-area'>" +
                f"<div class='widget-header'>❌ Error</div>" +
                f"<p>Error installing dependencies: {e}</p>" +
                f"</div>"
            )
            
            self.output_area.value = error_text
    
    def run_app(self, b):
        """Run the selected app"""
        try:
            if not self.selected_app:
                self.output_area.value = (
                    "<div class='output-area'>" +
                    "<div class='widget-header'>❌ Error</div>" +
                    "<p>No app selected</p>" +
                    "</div>"
                )
                return
            
            app = self.selected_app
            output_text = f"<div class='output-area'><div class='widget-header'>🚀 Running {app['name']}...</div>"
            
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
            
            output_text += "</div>"
            self.output_area.value = output_text
            
        except Exception as e:
            error_text = (
                f"<div class='output-area'>" +
                f"<div class='widget-header'>❌ Error</div>" +
                f"<p>Error running app: {e}</p>" +
                f"</div>"
            )
            
            self.output_area.value = error_text
        finally:
            # Change back to original directory
            os.chdir('/content')
    
    def get_streamlit_instructions(self, app):
        """Get instructions for running Streamlit apps"""
        return (
            "<h4>Streamlit App Detected</h4>" +
            "<p>To run this Streamlit app in Google Colab, use the following commands:</p>" +
            "<pre><code># Install ngrok for tunneling\n" +
            "!pip install streamlit pyngrok\n\n" +
            "# Set up ngrok tunnel\n" +
            "from pyngrok import ngrok\n" +
            "ngrok.set_auth_token(\"YOUR_NGROK_AUTH_TOKEN\")\n" +
            "public_url = ngrok.connect(8501)\n" +
            "print(f\"Streamlit app will be available at: {public_url}\")\n\n" +
            "# Run Streamlit in background\n" +
            "!nohup streamlit run app.py --server.port 8501 &</code></pre>"
        )
    
    def get_gradio_instructions(self, app):
        """Get instructions for running Gradio apps"""
        return (
            "<h4>Gradio App Detected</h4>" +
            "<p>To run this Gradio app in Google Colab, use the following commands:</p>" +
            "<pre><code># Install dependencies if needed\n" +
            "!pip install gradio\n\n" +
            "# Run the app (it will create a shareable link automatically)\n" +
            "import gradio as gr\n" +
            "# Import and run your gradio app here\n" +
            "# Or use: !python app.py</code></pre>"
        )
    
    def get_panel_instructions(self, app):
        """Get instructions for running Panel apps"""
        return (
            "<h4>Panel App Detected</h4>" +
            "<p>To run this Panel app in Google Colab, use the following commands:</p>" +
            "<pre><code># Install panel if needed\n" +
            "!pip install panel\n\n" +
            "# Import and run your panel app\n" +
            "import panel as pn\n" +
            "pn.extension(comms='colab')\n" +
            "# Import and run your panel app here</code></pre>"
        )
    
    def get_jupyter_instructions(self, app):
        """Get instructions for running Jupyter notebooks"""
        return (
            "<h4>Jupyter Notebook Detected</h4>" +
            "<p>To run this Jupyter notebook in Google Colab:</p>" +
            "<ol>" +
            "<li>Open the notebook file directly</li>" +
            "<li>Or use:</li>" +
            "</ol>" +
            "<pre><code># List available notebooks\n" +
            "!ls *.ipynb\n\n" +
            "# Run a specific notebook\n" +
            "!jupyter nbconvert --to notebook --execute your_notebook.ipynb</code></pre>"
        )
    
    def get_python_instructions(self, app):
        """Get instructions for running Python apps"""
        instructions = (
            "<h4>Python App Detected</h4>" +
            "<p>To run this Python app in Google Colab:</p>" +
            "<pre><code># Change to app directory\n" +
            f"%cd {app['path']}\n\n" +
            "# Install dependencies if available\n" +
            "!pip install -r requirements.txt 2>/dev/null || echo \"No requirements.txt found\"\n\n" +
            "# Run the app\n" +
            "!python main.py  # or app.py, depending on the main file</code></pre>" +
            "<h5>Main Python files found:</h5>" +
            "<ul>"
        )
        
        # List Python files
        try:
            py_files = list(Path(app['path']).rglob('*.py'))
            for py_file in py_files[:10]:  # Show first 10 Python files
                instructions += f"<li><code>{py_file.relative_to(app['path'])}</code></li>"
            
            if len(py_files) > 10:
                instructions += f"<li>... and {len(py_files) - 10} more files</li>"
        except Exception as e:
            instructions += f"<li>Error listing files: {e}</li>"
        
        instructions += "</ul>"
        return instructions
    
    def view_readme(self, b):
        """View the README file of the selected app"""
        try:
            if not self.selected_app:
                self.output_area.value = (
                    "<div class='output-area'>" +
                    "<div class='widget-header'>❌ Error</div>" +
                    "<p>No app selected</p>" +
                    "</div>"
                )
                return
            
            app = self.selected_app
            output_text = f"<div class='output-area'><div class='widget-header'>📖 README for {app['name']}</div>"
            
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
                output_text += f"<pre>{readme_content}</pre>"
            else:
                output_text += "<p>No README file found.</p>"
            
            output_text += "</div>"
            self.output_area.value = output_text
            
        except Exception as e:
            error_text = (
                f"<div class='output-area'>" +
                f"<div class='widget-header'>❌ Error</div>" +
                f"<p>Error reading README: {e}</p>" +
                f"</div>"
            )
            
            self.output_area.value = error_text
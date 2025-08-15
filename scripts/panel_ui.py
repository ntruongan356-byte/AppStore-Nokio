#!/usr/bin/env python3
"""
Panel UI components for the Colab App Store
This module contains the Panel-based user interface.
"""

import panel as pn
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional
import logging

# Import core functionality
from .app_store_core import ColabAppStoreCore

logger = logging.getLogger(__name__)


class PanelAppStoreUI:
    """Panel-based UI for the Colab App Store"""
    
    def __init__(self, core: ColabAppStoreCore):
        """
        Initialize the Panel UI
        
        Args:
            core: Core app store functionality instance
        """
        self.core = core
        self.setup_ui()
        
    def setup_ui(self):
        """Setup Panel UI components"""
        # Initialize Panel with Google Colab compatibility
        pn.extension(comms='colab', sizing_mode="stretch_width", template="material")
        pn.config.sizing_mode = "stretch_width"
        
        # UI Components
        self.status_display = pn.pane.Markdown(
            "###.create_status_display()
        )
        
        self.category_selector = pn.widgets.Select(
            name='Select Category',
            options=list(self.core.categories.keys()),
            value='1-Web-Development'
        )
        
        self.app_list_display = pn.pane.Markdown(
            "### 📋 App List\\n\\nSelect a category to view apps"
        )
        
        self.categorize_apps_btn = pn.widgets.Button(
            name='📂 Categorize All Apps',
            button_type='primary',
            disabled=False
        )
        
        self.clone_apps_btn = pn.widgets.Button(
            name='📥 Clone Apps to Categories',
            button_type='success',
            disabled=True
        )
        
        self.view_dashboard_btn = pn.widgets.Button(
            name='🎮 View App Dashboard',
            button_type='default',
            disabled=True
        )
        
        self.output_area = pn.pane.Markdown(
            "### 📋 Output\\n\\nReady to categorize apps..."
        )
        
        self.progress_bar = pn.widgets.Progress(
            name='Progress',
            bar_color='primary',
            value=0,
            max=100
        )
        
        # Bind events
        self.category_selector.param.watch(self.on_category_selected, 'value')
        self.categorize_apps_btn.on_click(self.categorize_apps)
        self.clone_apps_btn.on_click(self.clone_apps)
        self.view_dashboard_btn.on_click(self.view_dashboard)
        
        # Create layout
        self.create_layout()
    
    def create_status_display(self) -> str:
        """Create status display text"""
        return (
            "### 🚀 App Store Status\\n\\n" +
            "✅ Environment setup complete\\n" +
            "✅ Repository cloned\\n" +
            "✅ Panel UI loaded\\n" +
            "⏳ Ready to categorize apps"
        )
    
    def create_layout(self):
        """Create the main layout"""
        # Header section
        header_section = pn.Column(
            pn.pane.Markdown(self.create_header_text()),
            sizing_mode="stretch_width"
        )
        
        # Control section
        control_section = pn.Column(
            pn.pane.Markdown("### 🎮 Controls"),
            self.category_selector,
            self.categorize_apps_btn,
            self.clone_apps_btn,
            self.view_dashboard_btn,
            self.progress_bar,
            width=300
        )
        
        # Status section
        status_section = pn.Column(
            pn.pane.Markdown("### 📊 Status"),
            self.status_display,
            width=300
        )
        
        # Display section
        display_section = pn.Column(
            pn.pane.Markdown("### 📋 App List"),
            self.app_list_display,
            sizing_mode="stretch_width"
        )
        
        # Output section
        output_section = pn.Column(
            self.output_area,
            sizing_mode="stretch_width"
        )
        
        # Main layout
        self.layout = pn.Column(
            header_section,
            pn.Row(
                pn.Column(control_section, status_section, width=300),
                pn.Column(display_section, output_section, width=700)
            ),
            sizing_mode="stretch_width"
        )
    
    def create_header_text(self) -> str:
        """Create header text"""
        return (
            "# 🚀 Clean Colab App Store\\n\\n" +
            "### 📋 Instructions\\n" +
            "1. **Categorize Apps**: Click '📂 Categorize All Apps' to scan and categorize all apps\\n" +
            "2. **Clone Apps**: Click '📥 Clone Apps to Categories' to organize apps into folders\\n" +
            "3. **View Dashboard**: Click '🎮 View App Dashboard' to access the interactive app browser\\n" +
            "4. **Run Apps**: Use the dashboard to browse and run individual apps\\n\\n" +
            "### 🎯 Features\\n" +
            "- ✅ **Fast UI Loading**: Panel dashboard loads immediately\\n" +
            "- ✅ **Background Processing**: App categorization happens in background\\n" +
            "- ✅ **Clean Organization**: Apps organized by category\\n" +
            "- ✅ **Interactive Dashboard**: Browse and run apps with Panel UI\\n\\n" +
            "### 📁 Categories\\n" +
            "- **1-Web-Development**: Web development tools and applications\\n" +
            "- **2-Data-Science**: Data analysis and visualization tools\\n" +
            "- **3-Machine-Learning**: ML models and training tools\\n" +
            "- **4-Computer-Vision**: CV models and image processing\\n" +
            "- **5-Natural-Language-Processing**: NLP models and text processing\\n" +
            "- **6-Generative-AI**: GenAI models and content generation"
        )
    
    def on_category_selected(self, event):
        """Handle category selection"""
        if event.new:
            self.update_app_list_display()
    
    def update_app_list_display(self):
        """Update the app list display for selected category"""
        category = self.category_selector.value
        
        if not self.core.apps:
            self.app_list_display.object = (
                f"### 📋 App List\\n\\n" +
                "No apps categorized yet. Click '📂 Categorize All Apps' first."
            )
            return
        
        # Get apps for this category
        category_apps = [app for app in self.core.apps if app.get('category') == category]
        
        if not category_apps:
            self.app_list_display.object = (
                f"### 📋 App List\\n\\n" +
                f"No apps found in category: {category}"
            )
            return
        
        # Create app list display
        app_list = f"### 📋 App List - {category}\\n\\n"
        
        for app in category_apps:
            app_list += (
                f"**{app.get('name', 'Unknown')}**\\n" +
                f"- Type: {app.get('type', 'Unknown')}\\n" +
                f"- Size: {self.core.format_size(app.get('size', 0))}\\n" +
                f"- Path: {app.get('path', 'Unknown')}\\n\\n"
            )
        
        self.app_list_display.object = app_list
    
    def categorize_apps(self, event):
        """Categorize all apps in the repository"""
        self.output_area.object = "### 📂 Categorizing Apps...\\n\\n"
        self.categorize_apps_btn.disabled = True
        
        try:
            # Scan repository for apps
            self.core.apps = self.core.scan_repository_for_apps()
            
            # Update progress
            self.progress_bar.value = 100
            
            # Update display
            self.output_area.object = (
                f"### ✅ Categorization Complete!\\n\\n" +
                f"Found {len(self.core.apps)} apps across {len(self.core.categories)} categories.\\n\\n" +
                f"### 📊 Category Summary\\n\\n"
            )
            
            # Show category summary
            for category, subcategories in self.core.categories.items():
                category_count = len([app for app in self.core.apps if app.get('category') == category])
                self.output_area.object += f"**{category}**: {category_count} apps\\n"
            
            # Enable buttons
            self.clone_apps_btn.disabled = False
            self.view_dashboard_btn.disabled = False
            
            # Update app list display
            self.update_app_list_display()
            
        except Exception as e:
            self.output_area.object = f"### ❌ Error categorizing apps: {e}\\n"
            self.categorize_apps_btn.disabled = False
    
    def clone_apps(self, event):
        """Clone apps to their respective category folders"""
        self.output_area.object = "### 📥 Cloning Apps to Categories...\\n\\n"
        self.clone_apps_btn.disabled = True
        
        try:
            # Create symlinks or copy apps to category folders
            success = self.core.organize_apps_into_categories()
            
            if success:
                self.output_area.object = (
                    f"### ✅ Apps Cloned Successfully!\\n\\n" +
                    f"{len(self.core.apps)} apps organized into {len(self.core.categories)} categories.\\n\\n" +
                    f"### 📁 Category Structure\\n\\n"
                )
                
                # Show category structure
                for category in self.core.categories.keys():
                    category_path = Path(f"Pinokio-Apps/{category}")
                    if category_path.exists():
                        app_count = len(list(category_path.iterdir()))
                        self.output_area.object += f"**{category}**: {app_count} apps\\n"
                
                self.view_dashboard_btn.disabled = False
            
        except Exception as e:
            self.output_area.object = f"### ❌ Error cloning apps: {e}\\n"
            self.clone_apps_btn.disabled = False
    
    def view_dashboard(self, event):
        """View the interactive app dashboard"""
        self.output_area.object = "### 🎮 Loading Interactive Dashboard...\\n\\n"
        
        try:
            # Import and create the dashboard
            from .interactive_dashboard import InteractiveDashboard
            
            # Create dashboard instance
            dashboard = InteractiveDashboard(self.core)
            
            # Get the dashboard layout
            dashboard_layout = dashboard.create_dashboard()
            
            # Display the dashboard
            self.output_area.object = "### 🎮 Interactive App Dashboard\\n\\n" +
                                           "Use the dashboard below to browse and run apps:\\n\\n"
            
            # Add the dashboard to the output
            self.output_area.object += dashboard_layout
            
        except Exception as e:
            self.output_area.object = f"### ❌ Error loading dashboard: {e}\\n"
    
    def show(self):
        """Display the app store"""
        return self.layout


class InteractiveDashboard:
    """Interactive dashboard for browsing and running apps"""
    
    def __init__(self, core: ColabAppStoreCore):
        """
        Initialize the interactive dashboard
        
        Args:
            core: Core app store functionality instance
        """
        self.core = core
        self.selected_app = None
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the dashboard UI components"""
        # App selector
        self.app_selector = pn.widgets.Select(
            name='Select App',
            options=[],
            value=None
        )
        
        # Search filter
        self.search_box = pn.widgets.TextInput(
            name='Search Apps',
            placeholder='Type to filter apps...'
        )
        
        # Type filter
        self.type_filter = pn.widgets.MultiSelect(
            name='Filter by Type',
            options=[],
            value=[]
        )
        
        # Category filter
        self.category_filter = pn.widgets.MultiSelect(
            name='Filter by Category',
            options=list(self.core.categories.keys()),
            value=list(self.core.categories.keys())
        )
        
        # App details display
        self.app_details = pn.pane.Markdown("Select an app to view details")
        
        # Action buttons
        self.install_deps_btn = pn.widgets.Button(
            name='Install Dependencies',
            button_type='primary',
            disabled=True
        )
        
        self.run_app_btn = pn.widgets.Button(
            name='Run App',
            button_type='success',
            disabled=True
        )
        
        self.view_readme_btn = pn.widgets.Button(
            name='View README',
            button_type='default',
            disabled=True
        )
        
        # Output area
        self.output_area = pn.pane.Markdown("### Output\\n")
        
        # Bind events
        self.app_selector.param.watch(self.on_app_selected, 'value')
        self.search_box.param.watch(self.on_search_changed, 'value')
        self.type_filter.param.watch(self.on_type_filter_changed, 'value')
        self.category_filter.param.watch(self.on_category_filter_changed, 'value')
        self.install_deps_btn.on_click(self.install_dependencies)
        self.run_app_btn.on_click(self.run_app)
        self.view_readme_btn.on_click(self.view_readme)
        
        # Update filter options
        self.update_filter_options()
    
    def update_filter_options(self):
        """Update filter options based on available apps"""
        if self.core.apps:
            # Update type filter options
            app_types = list(set(app['type'] for app in self.core.apps))
            self.type_filter.options = app_types
            self.type_filter.value = app_types
            
            # Update app selector options
            self.update_app_selector_options()
    
    def update_app_selector_options(self):
        """Update the app selector options based on filters"""
        filtered_apps = self.core.apps
        
        # Apply search filter
        if self.search_box.value:
            search_term = self.search_box.value.lower()
            filtered_apps = [app for app in filtered_apps 
                           if search_term in app['name'].lower()]
        
        # Apply type filter
        if self.type_filter.value:
            filtered_apps = [app for app in filtered_apps 
                           if app['type'] in self.type_filter.value]
        
        # Apply category filter
        if self.category_filter.value:
            filtered_apps = [app for app in filtered_apps 
                           if app['category'] in self.category_filter.value]
        
        self.app_selector.options = [app['name'] for app in filtered_apps]
        
        # Update selection if current selection is not in filtered list
        if self.app_selector.value and self.app_selector.value not in self.app_selector.options:
            self.app_selector.value = self.app_selector.options[0] if self.app_selector.options else None
    
    def on_app_selected(self, event):
        """Handle app selection"""
        if event.new:
            self.selected_app = next((app for app in self.core.apps if app['name'] == event.new), None)
            self.update_app_details()
            self.update_button_states()
    
    def on_search_changed(self, event):
        """Handle search filter"""
        self.update_app_selector_options()
    
    def on_type_filter_changed(self, event):
        """Handle type filter"""
        self.update_app_selector_options()
    
    def on_category_filter_changed(self, event):
        """Handle category filter"""
        self.update_app_selector_options()
    
    def update_app_details(self):
        """Update the app details display"""
        if not self.selected_app:
            self.app_details.object = "Select an app to view details"
            return
        
        app = self.selected_app
        details = (
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
                    details += f"- `{file.relative_to(app['path'])}`\\n"
        except Exception as e:
            details += f"Error listing files: {e}\\n"
        
        self.app_details.object = details
    
    def update_button_states(self):
        """Update button states based on selected app"""
        if not self.selected_app:
            self.install_deps_btn.disabled = True
            self.run_app_btn.disabled = True
            self.view_readme_btn.disabled = True
            return
        
        app = self.selected_app
        self.install_deps_btn.disabled = not app['has_requirements']
        self.view_readme_btn.disabled = not app['has_readme']
        self.run_app_btn.disabled = False  # Always enable run button
    
    def install_dependencies(self, event):
        """Install dependencies for the selected app"""
        if not self.selected_app:
            return
        
        app = self.selected_app
        self.output_area.object = f"### Installing dependencies for {app['name']}...\\n\\n"
        
        try:
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
                    self.output_area.object += f"```\\n{result.stdout}\\n```\\n"
                    if result.stderr:
                        self.output_area.object += f"**Errors:**\\n```\\n{result.stderr}\\n```\\n"
                else:
                    self.output_area.object += f"Requirements file found: {req_file.name}\\n"
                    self.output_area.object += "Please install dependencies manually for this file type.\\n"
            else:
                self.output_area.object += "No requirements file found.\\n"
                
        except Exception as e:
            self.output_area.object += f"Error installing dependencies: {e}\\n"
    
    def run_app(self, event):
        """Run the selected app"""
        if not self.selected_app:
            return
        
        app = self.selected_app
        self.output_area.object = f"### Running {app['name']}...\\n\\n"
        
        try:
            # Change to app directory
            os.chdir(app['path'])
            
            # Determine how to run the app based on its type
            if app['type'] == 'streamlit':
                self.output_area.object += self.get_streamlit_instructions(app)
            elif app['type'] == 'gradio':
                self.output_area.object += self.get_gradio_instructions(app)
            elif app['type'] == 'panel':
                self.output_area.object += self.get_panel_instructions(app)
            elif app['type'] == 'jupyter':
                self.output_area.object += self.get_jupyter_instructions(app)
            else:
                # Generic Python app
                self.output_area.object += self.get_python_instructions(app)
            
        except Exception as e:
            self.output_area.object += f"Error running app: {e}\\n"
        
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
    
    def view_readme(self, event):
        """View the README file of the selected app"""
        if not self.selected_app:
            return
        
        app = self.selected_app
        self.output_area.object = f"### README for {app['name']}\\n\\n"
        
        try:
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
                self.output_area.object += f"```\\n{readme_content}\\n```"
            else:
                self.output_area.object += "No README file found.\\n"
                
        except Exception as e:
            self.output_area.object += f"Error reading README: {e}\\n"
    
    def create_dashboard(self):
        """Create the dashboard layout"""
        # Filter section
        filter_section = pn.Column(
            pn.pane.Markdown("### Filters"),
            self.search_box,
            self.type_filter,
            self.category_filter
        )
        
        # App selection section
        selection_section = pn.Column(
            pn.pane.Markdown("### App Selection"),
            self.app_selector,
            self.install_deps_btn,
            self.run_app_btn,
            self.view_readme_btn
        )
        
        # Details section
        details_section = pn.Column(
            pn.pane.Markdown("### App Details"),
            self.app_details
        )
        
        # Output section
        output_section = pn.Column(
            self.output_area
        )
        
        # Main layout
        return pn.Row(
            pn.Column(filter_section, selection_section, width=300),
            pn.Column(details_section, output_section, width=700)
        )
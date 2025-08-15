/**
 * Clean Colab App Store - JavaScript Functions
 * This file contains client-side JavaScript functionality for the app store.
 */

// Global variables
let appStoreCore = null;
let currentUI = null;

/**
 * Initialize the app store when the page loads
 */
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Initializing Clean Colab App Store...');
    initializeAppStore();
});

/**
 * Initialize the app store core functionality
 */
function initializeAppStore() {
    try {
        // Check if we're in Google Colab
        if (isGoogleColab()) {
            console.log('📱 Running in Google Colab environment');
            setupColabCompatibility();
        }
        
        // Initialize UI components
        setupUIComponents();
        
        // Setup event listeners
        setupEventListeners();
        
        console.log('✅ App Store initialized successfully');
        
    } catch (error) {
        console.error('❌ Error initializing app store:', error);
        showError('Failed to initialize app store: ' + error.message);
    }
}

/**
 * Check if we're running in Google Colab
 */
function isGoogleColab() {
    try {
        // Check for Colab-specific global variables
        return typeof google !== 'undefined' && 
               typeof google.colab !== 'undefined' &&
               typeof google.colab.kernel !== 'undefined';
    } catch (e) {
        return false;
    }
}

/**
 * Setup Google Colab compatibility
 */
function setupColabCompatibility() {
    try {
        // Configure Panel for Colab compatibility
        if (typeof panel !== 'undefined') {
            panel.extension(comms='colab', sizing_mode="stretch_width", template="material");
            panel.config.sizing_mode = "stretch_width";
        }
        
        // Add Colab-specific CSS
        addColabStyles();
        
        console.log('✅ Google Colab compatibility setup complete');
        
    } catch (error) {
        console.error('❌ Error setting up Colab compatibility:', error);
    }
}

/**
 * Add Colab-specific styles
 */
function addColabStyles() {
    const style = document.createElement('style');
    style.textContent = `
        /* Colab-specific styles */
        .gradio-container {
            max-width: 100% !important;
            margin: 0 !important;
        }
        
        .panel-container {
            max-width: 100% !important;
            margin: 0 !important;
        }
        
        /* Responsive adjustments for Colab */
        @media (max-width: 768px) {
            .widget-container {
                width: 100% !important;
                margin: 5px 0 !important;
            }
        }
    `;
    document.head.appendChild(style);
}

/**
 * Setup UI components
 */
function setupUIComponents() {
    try {
        // Setup button event listeners
        setupButtonListeners();
        
        // Setup filter components
        setupFilterComponents();
        
        // Setup progress indicators
        setupProgressIndicators();
        
        // Setup output areas
        setupOutputAreas();
        
        console.log('✅ UI components setup complete');
        
    } catch (error) {
        console.error('❌ Error setting up UI components:', error);
    }
}

/**
 * Setup button event listeners
 */
function setupButtonListeners() {
    try {
        // Categorize apps button
        const categorizeBtn = document.querySelector('#categorize-apps-btn');
        if (categorizeBtn) {
            categorizeBtn.addEventListener('click', handleCategorizeApps);
        }
        
        // Clone apps button
        const cloneBtn = document.querySelector('#clone-apps-btn');
        if (cloneBtn) {
            cloneBtn.addEventListener('click', handleCloneApps);
        }
        
        // View dashboard button
        const viewDashboardBtn = document.querySelector('#view-dashboard-btn');
        if (viewDashboardBtn) {
            viewDashboardBtn.addEventListener('click', handleViewDashboard);
        }
        
        // Install dependencies button
        const installDepsBtn = document.querySelector('#install-deps-btn');
        if (installDepsBtn) {
            installDepsBtn.addEventListener('click', handleInstallDependencies);
        }
        
        // Run app button
        const runAppBtn = document.querySelector('#run-app-btn');
        if (runAppBtn) {
            runAppBtn.addEventListener('click', handleRunApp);
        }
        
        // View README button
        const viewReadmeBtn = document.querySelector('#view-readme-btn');
        if (viewReadmeBtn) {
            viewReadmeBtn.addEventListener('click', handleViewReadme);
        }
        
        console.log('✅ Button listeners setup complete');
        
    } catch (error) {
        console.error('❌ Error setting up button listeners:', error);
    }
}

/**
 * Setup filter components
 */
function setupFilterComponents() {
    try {
        // Search box
        const searchBox = document.querySelector('#search-box');
        if (searchBox) {
            searchBox.addEventListener('input', debounce(handleSearchFilter, 300));
        }
        
        // Category filter
        const categoryFilter = document.querySelector('#category-filter');
        if (categoryFilter) {
            categoryFilter.addEventListener('change', handleCategoryFilter);
        }
        
        // Type filter
        const typeFilter = document.querySelector('#type-filter');
        if (typeFilter) {
            typeFilter.addEventListener('change', handleTypeFilter);
        }
        
        // App selector
        const appSelector = document.querySelector('#app-selector');
        if (appSelector) {
            appSelector.addEventListener('change', handleAppSelection);
        }
        
        console.log('✅ Filter components setup complete');
        
    } catch (error) {
        console.error('❌ Error setting up filter components:', error);
    }
}

/**
 * Setup progress indicators
 */
function setupProgressIndicators() {
    try {
        // Progress bar
        const progressBar = document.querySelector('#progress-bar');
        if (progressBar) {
            // Initialize progress bar
            progressBar.style.width = '0%';
        }
        
        // Status display
        const statusDisplay = document.querySelector('#status-display');
        if (statusDisplay) {
            // Initialize status display
            updateStatusDisplay('Ready to categorize apps...');
        }
        
        console.log('✅ Progress indicators setup complete');
        
    } catch (error) {
        console.error('❌ Error setting up progress indicators:', error);
    }
}

/**
 * Setup output areas
 */
function setupOutputAreas() {
    try {
        // Output area
        const outputArea = document.querySelector('#output-area');
        if (outputArea) {
            // Initialize output area
            outputArea.innerHTML = '<div class="widget-header">📋 Output</div><div>Ready to categorize apps...</div>';
        }
        
        // App details area
        const appDetails = document.querySelector('#app-details');
        if (appDetails) {
            // Initialize app details area
            appDetails.innerHTML = '<div class="widget-header">📋 App Details</div><div>Select an app to view details</div>';
        }
        
        console.log('✅ Output areas setup complete');
        
    } catch (error) {
        console.error('❌ Error setting up output areas:', error);
    }
}

/**
 * Setup event listeners
 */
function setupEventListeners() {
    try {
        // Handle window resize
        window.addEventListener('resize', debounce(handleWindowResize, 250));
        
        // Handle keyboard shortcuts
        document.addEventListener('keydown', handleKeyboardShortcuts);
        
        // Handle visibility changes
        document.addEventListener('visibilitychange', handleVisibilityChange);
        
        console.log('✅ Event listeners setup complete');
        
    } catch (error) {
        console.error('❌ Error setting up event listeners:', error);
    }
}

/**
 * Handle categorize apps button click
 */
async function handleCategorizeApps() {
    try {
        console.log('📂 Categorizing apps...');
        
        // Update UI
        updateStatusDisplay('Categorizing apps...');
        updateProgressBar(0);
        disableButton('categorize-apps-btn', true);
        
        // Simulate app categorization (in real implementation, this would call Python backend)
        await simulateAppCategorization();
        
        // Update UI
        updateStatusDisplay('Apps categorized successfully!');
        updateProgressBar(100);
        enableButton('clone-apps-btn', false);
        enableButton('view-dashboard-btn', false);
        
        console.log('✅ App categorization complete');
        
    } catch (error) {
        console.error('❌ Error categorizing apps:', error);
        showError('Failed to categorize apps: ' + error.message);
        enableButton('categorize-apps-btn', false);
    }
}

/**
 * Handle clone apps button click
 */
async function handleCloneApps() {
    try {
        console.log('📥 Cloning apps to categories...');
        
        // Update UI
        updateStatusDisplay('Cloning apps to categories...');
        updateProgressBar(0);
        disableButton('clone-apps-btn', true);
        
        // Simulate app cloning (in real implementation, this would call Python backend)
        await simulateAppCloning();
        
        // Update UI
        updateStatusDisplay('Apps cloned successfully!');
        updateProgressBar(100);
        enableButton('view-dashboard-btn', false);
        
        console.log('✅ App cloning complete');
        
    } catch (error) {
        console.error('❌ Error cloning apps:', error);
        showError('Failed to clone apps: ' + error.message);
        enableButton('clone-apps-btn', false);
    }
}

/**
 * Handle view dashboard button click
 */
function handleViewDashboard() {
    try {
        console.log('🎮 Viewing dashboard...');
        
        // Update UI
        updateStatusDisplay('Loading dashboard...');
        
        // In real implementation, this would load the interactive dashboard
        loadInteractiveDashboard();
        
        console.log('✅ Dashboard loaded');
        
    } catch (error) {
        console.error('❌ Error viewing dashboard:', error);
        showError('Failed to load dashboard: ' + error.message);
    }
}

/**
 * Handle install dependencies button click
 */
async function handleInstallDependencies() {
    try {
        console.log('📦 Installing dependencies...');
        
        // Get selected app
        const selectedApp = getSelectedApp();
        if (!selectedApp) {
            showError('No app selected');
            return;
        }
        
        // Update UI
        updateOutputArea(`Installing dependencies for ${selectedApp.name}...`);
        disableButton('install-deps-btn', true);
        
        // Simulate dependency installation
        await simulateDependencyInstallation(selectedApp);
        
        // Update UI
        updateOutputArea(`Dependencies installed successfully for ${selectedApp.name}!`);
        enableButton('install-deps-btn', false);
        
        console.log('✅ Dependencies installed');
        
    } catch (error) {
        console.error('❌ Error installing dependencies:', error);
        showError('Failed to install dependencies: ' + error.message);
        enableButton('install-deps-btn', false);
    }
}

/**
 * Handle run app button click
 */
function handleRunApp() {
    try {
        console.log('🚀 Running app...');
        
        // Get selected app
        const selectedApp = getSelectedApp();
        if (!selectedApp) {
            showError('No app selected');
            return;
        }
        
        // Update UI
        updateOutputArea(`Running ${selectedApp.name}...`);
        
        // Generate app running instructions
        const instructions = generateAppInstructions(selectedApp);
        updateOutputArea(instructions);
        
        console.log('✅ App running instructions generated');
        
    } catch (error) {
        console.error('❌ Error running app:', error);
        showError('Failed to run app: ' + error.message);
    }
}

/**
 * Handle view README button click
 */
function handleViewReadme() {
    try {
        console.log('📖 Viewing README...');
        
        // Get selected app
        const selectedApp = getSelectedApp();
        if (!selectedApp) {
            showError('No app selected');
            return;
        }
        
        // Update UI
        updateOutputArea(`Loading README for ${selectedApp.name}...`);
        
        // Simulate README loading
        const readmeContent = await simulateReadmeLoading(selectedApp);
        updateOutputArea(readmeContent);
        
        console.log('✅ README loaded');
        
    } catch (error) {
        console.error('❌ Error viewing README:', error);
        showError('Failed to load README: ' + error.message);
    }
}

/**
 * Handle search filter
 */
function handleSearchFilter(event) {
    try {
        const searchTerm = event.target.value.toLowerCase();
        console.log('🔍 Searching for:', searchTerm);
        
        // Filter apps based on search term
        filterApps(searchTerm);
        
    } catch (error) {
        console.error('❌ Error handling search filter:', error);
    }
}

/**
 * Handle category filter
 */
function handleCategoryFilter(event) {
    try {
        const selectedCategories = Array.from(event.target.selectedOptions).map(option => option.value);
        console.log('📁 Selected categories:', selectedCategories);
        
        // Filter apps based on selected categories
        filterAppsByCategory(selectedCategories);
        
    } catch (error) {
        console.error('❌ Error handling category filter:', error);
    }
}

/**
 * Handle type filter
 */
function handleTypeFilter(event) {
    try {
        const selectedTypes = Array.from(event.target.selectedOptions).map(option => option.value);
        console.log('🔧 Selected types:', selectedTypes);
        
        // Filter apps based on selected types
        filterAppsByType(selectedTypes);
        
    } catch (error) {
        console.error('❌ Error handling type filter:', error);
    }
}

/**
 * Handle app selection
 */
function handleAppSelection(event) {
    try {
        const selectedAppName = event.target.value;
        console.log('📋 Selected app:', selectedAppName);
        
        // Update app details
        updateAppDetails(selectedAppName);
        
        // Update button states
        updateButtonStates(selectedAppName);
        
    } catch (error) {
        console.error('❌ Error handling app selection:', error);
    }
}

/**
 * Handle window resize
 */
function handleWindowResize() {
    try {
        // Adjust UI components for window size
        adjustUIForWindowSize();
        
    } catch (error) {
        console.error('❌ Error handling window resize:', error);
    }
}

/**
 * Handle keyboard shortcuts
 */
function handleKeyboardShortcuts(event) {
    try {
        // Handle specific keyboard shortcuts
        switch (event.key) {
            case 'Enter':
                if (event.ctrlKey) {
                    // Ctrl+Enter: Run selected app
                    handleRunApp();
                }
                break;
            case 'Escape':
                // Escape: Clear filters
                clearFilters();
                break;
        }
        
    } catch (error) {
        console.error('❌ Error handling keyboard shortcuts:', error);
    }
}

/**
 * Handle visibility change
 */
function handleVisibilityChange() {
    try {
        if (document.hidden) {
            // Page is hidden, pause any animations or processes
            console.log('📱 Page hidden, pausing processes');
        } else {
            // Page is visible, resume processes
            console.log('📱 Page visible, resuming processes');
        }
        
    } catch (error) {
        console.error('❌ Error handling visibility change:', error);
    }
}

/**
 * Utility Functions
 */

/**
 * Debounce function to limit how often a function is called
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Update status display
 */
function updateStatusDisplay(message) {
    const statusDisplay = document.querySelector('#status-display');
    if (statusDisplay) {
        statusDisplay.innerHTML = `<div class="widget-header">📊 Status</div><div>${message}</div>`;
    }
}

/**
 * Update progress bar
 */
function updateProgressBar(percentage) {
    const progressBar = document.querySelector('#progress-bar');
    if (progressBar) {
        progressBar.style.width = `${percentage}%`;
    }
}

/**
 * Update output area
 */
function updateOutputArea(content) {
    const outputArea = document.querySelector('#output-area');
    if (outputArea) {
        outputArea.innerHTML = `<div class="widget-header">📋 Output</div><div>${content}</div>`;
    }
}

/**
 * Update app details
 */
function updateAppDetails(appName) {
    const appDetails = document.querySelector('#app-details');
    if (appDetails) {
        // In real implementation, this would fetch app details
        appDetails.innerHTML = `<div class="widget-header">📋 App Details</div><div>Loading details for ${appName}...</div>`;
    }
}

/**
 * Disable button
 */
function disableButton(buttonId, disabled = true) {
    const button = document.querySelector(`#${buttonId}`);
    if (button) {
        button.disabled = disabled;
        button.classList.toggle('disabled', disabled);
    }
}

/**
 * Enable button
 */
function enableButton(buttonId, disabled = false) {
    disableButton(buttonId, disabled);
}

/**
 * Show error message
 */
function showError(message) {
    const outputArea = document.querySelector('#output-area');
    if (outputArea) {
        outputArea.innerHTML = `<div class="widget-header">❌ Error</div><div class="status-error">${message}</div>`;
    }
}

/**
 * Get selected app
 */
function getSelectedApp() {
    const appSelector = document.querySelector('#app-selector');
    if (appSelector && appSelector.value) {
        return {
            name: appSelector.value,
            type: 'unknown' // In real implementation, this would be fetched
        };
    }
    return null;
}

/**
 * Generate app instructions
 */
function generateAppInstructions(app) {
    // In real implementation, this would generate specific instructions based on app type
    return `<h4>Running ${app.name}</h4>
<p>This is a ${app.type} application.</p>
<h5>Instructions:</h5>
<pre><code># Change to app directory
%cd ${app.path}

# Install dependencies if available
!pip install -r requirements.txt

# Run the app
!python main.py</code></pre>`;
}

/**
 * Simulation Functions (for demo purposes)
 */

/**
 * Simulate app categorization
 */
async function simulateAppCategorization() {
    return new Promise((resolve) => {
        let progress = 0;
        const interval = setInterval(() => {
            progress += 10;
            updateProgressBar(progress);
            if (progress >= 100) {
                clearInterval(interval);
                resolve();
            }
        }, 200);
    });
}

/**
 * Simulate app cloning
 */
async function simulateAppCloning() {
    return new Promise((resolve) => {
        let progress = 0;
        const interval = setInterval(() => {
            progress += 20;
            updateProgressBar(progress);
            if (progress >= 100) {
                clearInterval(interval);
                resolve();
            }
        }, 150);
    });
}

/**
 * Simulate dependency installation
 */
async function simulateDependencyInstallation(app) {
    return new Promise((resolve) => {
        setTimeout(() => {
            resolve();
        }, 1000);
    });
}

/**
 * Simulate README loading
 */
async function simulateReadmeLoading(app) {
    return new Promise((resolve) => {
        setTimeout(() => {
            resolve(`<h4>README for ${app.name}</h4>
<p>This is a simulated README file for ${app.name}.</p>
<h5>Description:</h5>
<p>${app.name} is a ${app.type} application.</p>
<h5>Installation:</h5>
<pre><code>pip install -r requirements.txt</code></pre>
<h5>Usage:</h5>
<pre><code>python main.py</code></pre>`);
        }, 500);
    });
}

/**
 * Load interactive dashboard
 */
function loadInteractiveDashboard() {
    // In real implementation, this would load the actual dashboard
    updateOutputArea(`
        <div class="widget-header">🎮 Interactive App Dashboard</div>
        <div>Use the dashboard below to browse and run apps:</div>
        <div class="app-list">
            <div class="app-list-item">📱 Example App 1</div>
            <div class="app-list-item">🤖 Example App 2</div>
            <div class="app-list-item">📊 Example App 3</div>
        </div>
    `);
}

/**
 * Filter apps based on search term
 */
function filterApps(searchTerm) {
    // In real implementation, this would filter the actual app list
    console.log('Filtering apps by:', searchTerm);
}

/**
 * Filter apps by category
 */
function filterAppsByCategory(categories) {
    // In real implementation, this would filter apps by selected categories
    console.log('Filtering apps by categories:', categories);
}

/**
 * Filter apps by type
 */
function filterAppsByType(types) {
    // In real implementation, this would filter apps by selected types
    console.log('Filtering apps by types:', types);
}

/**
 * Update button states based on selected app
 */
function updateButtonStates(appName) {
    // In real implementation, this would update button states based on app properties
    console.log('Updating button states for:', appName);
}

/**
 * Clear all filters
 */
function clearFilters() {
    // Clear search box
    const searchBox = document.querySelector('#search-box');
    if (searchBox) {
        searchBox.value = '';
    }
    
    // Clear category filter
   Filter = const category document.querySelector('#category-filter');
    if (categoryFilter) {
        categoryFilter.selectedIndex = -1;
    }
    
    // Clear type filter
    const typeFilter = document.querySelector('#type-filter');
    if (typeFilter) {
        typeFilter.selectedIndex = -1;
    }
    
    // Trigger filter update
    filterApps('');
}

/**
 * Adjust UI for window size
 */
function adjustUIForWindowSize() {
    const width = window.innerWidth;
    console.log('Adjusting UI for window width:', width);
    
    // In real implementation, this would adjust UI components based on window size
    if (width < 768) {
        // Mobile adjustments
        document.body.classList.add('mobile-view');
    } else {
        document.body.classList.remove('mobile-view');
    }
}

// Export functions for global access
window.appStore = {
    initializeAppStore,
    handleCategorizeApps,
    handleCloneApps,
    handleViewDashboard,
    handleInstallDependencies,
    handleRunApp,
    handleViewReadme,
    clearFilters
};
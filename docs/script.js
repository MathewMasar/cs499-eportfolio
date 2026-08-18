document.addEventListener("DOMContentLoaded", () => {

    // ========================================================
    // GENERIC MARKDOWN LOADER
    // ========================================================

    async function loadMarkdown(path, target, errorMessage) {

        if (!path || !target) {
            return;
        }

        try {

            const response = await fetch(path);

            if (!response.ok) {
                throw new Error(
                    `Request failed with status ${response.status}`
                );
            }

            const markdown = await response.text();

            if (!window.marked) {
                throw new Error(
                    "Marked library is unavailable."
                );
            }

            target.innerHTML = marked.parse(markdown);

        } catch (error) {

            target.textContent = errorMessage;

            console.error(
                errorMessage,
                error
            );
        }
    }


    // ========================================================
    // HOME PAGE
    // PROFESSIONAL SELF-ASSESSMENT
    // ========================================================

    const selfAssessmentContent =
        document.getElementById(
            "self-assessment-content"
        );

    if (selfAssessmentContent) {

        loadMarkdown(
            "professional-self-assessment.md",
            selfAssessmentContent,
            "Unable to load Professional Self-Assessment."
        );
    }


    // ========================================================
    // ARTIFACT PAGES ONLY
    // ========================================================

    const body = document.body;

    if (!body.classList.contains("artifact-page")) {
        return;
    }


    // ========================================================
    // ARTIFACT CONFIGURATION
    // ========================================================

    const enhancedBase =
        body.dataset.artifactBase;

    const originalBase =
        body.dataset.originalBase;

    const readmeFile =
        body.dataset.readme;

    const narrativeFile =
        body.dataset.narrative;

    const language =
        body.dataset.language || "plaintext";

    const enhancedDefaultFile =
        body.dataset.defaultFile;

    const originalDefaultFile =
        body.dataset.originalDefaultFile;


    // ========================================================
    // ENHANCEMENT NARRATIVE
    // ========================================================

    const narrativeContent =
        document.getElementById(
            "narrative-content"
        );

    if (
        narrativeFile &&
        narrativeContent
    ) {

        loadMarkdown(
            narrativeFile,
            narrativeContent,
            "Unable to load enhancement narrative."
        );
    }


    // ========================================================
    // README
    // ========================================================

    const readmeContent =
        document.getElementById(
            "readme-content"
        );

    if (
        enhancedBase &&
        readmeFile &&
        readmeContent
    ) {

        loadMarkdown(
            enhancedBase + readmeFile,
            readmeContent,
            "Unable to load README."
        );
    }


    // ========================================================
    // SOURCE CODE LOADER
    // ========================================================

    async function loadCode(
        basePath,
        file,
        target
    ) {

        if (
            !basePath ||
            !file ||
            !target
        ) {
            return;
        }

        try {

            const response =
                await fetch(
                    basePath + file
                );

            if (!response.ok) {

                throw new Error(
                    `Source request failed with status ${response.status}`
                );
            }

            const code =
                await response.text();

            target.textContent =
                code;


            // Jupyter Notebook files are JSON documents,
            // so highlight them as JSON instead of Python.

            if (
                file
                    .toLowerCase()
                    .endsWith(".ipynb")
            ) {

                target.className =
                    "language-json";

            } else {

                target.className =
                    `language-${language}`;
            }


            // Apply Prism syntax highlighting.

            if (window.Prism) {

                Prism.highlightElement(
                    target
                );
            }

        } catch (error) {

            target.textContent =
                "Unable to load source file.";

            console.error(
                "Source loading failed:",
                error
            );
        }
    }


    // ========================================================
    // ARTIFACT VIEWER TABS
    // ========================================================

    const tabs =
        document.querySelectorAll(
            ".viewer-tab"
        );

    const panels =
        document.querySelectorAll(
            ".viewer-panel"
        );

    tabs.forEach(button => {

        button.addEventListener(
            "click",
            () => {

                // Hide all panels.

                panels.forEach(panel => {

                    panel.classList.add(
                        "hidden"
                    );
                });


                // Remove active styling from all tabs.

                tabs.forEach(tab => {

                    tab.classList.remove(
                        "active-tab"
                    );
                });


                // Find the panel associated
                // with the selected tab.

                const target =
                    document.getElementById(
                        button.dataset.panel
                    );


                // Display selected panel.

                if (target) {

                    target.classList.remove(
                        "hidden"
                    );
                }


                // Highlight selected tab.

                button.classList.add(
                    "active-tab"
                );
            }
        );
    });


    // ========================================================
    // ENHANCED SOURCE CODE VIEWER
    // ========================================================

    const enhancedSelect =
        document.getElementById(
            "enhanced-source-file"
        );

    const enhancedCode =
        document.getElementById(
            "enhanced-source-code"
        );

    if (
        enhancedSelect &&
        enhancedCode
    ) {

        // Load the default enhanced file.

        if (enhancedDefaultFile) {

            enhancedSelect.value =
                enhancedDefaultFile;

            loadCode(
                enhancedBase,
                enhancedDefaultFile,
                enhancedCode
            );
        }


        // Load another enhanced file
        // when selected from the dropdown.

        enhancedSelect.addEventListener(
            "change",
            event => {

                loadCode(
                    enhancedBase,
                    event.target.value,
                    enhancedCode
                );
            }
        );
    }


    // ========================================================
    // ORIGINAL SOURCE CODE VIEWER
    // ========================================================

    const originalSelect =
        document.getElementById(
            "original-source-file"
        );

    const originalCode =
        document.getElementById(
            "original-source-code"
        );

    if (
        originalSelect &&
        originalCode
    ) {

        // Load the default original file.

        if (originalDefaultFile) {

            originalSelect.value =
                originalDefaultFile;

            loadCode(
                originalBase,
                originalDefaultFile,
                originalCode
            );
        }


        // Load another original file
        // when selected from the dropdown.

        originalSelect.addEventListener(
            "change",
            event => {

                loadCode(
                    originalBase,
                    event.target.value,
                    originalCode
                );
            }
        );
    }

});
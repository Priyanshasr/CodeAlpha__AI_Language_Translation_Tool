/**
 * LinguaBridge AI — Frontend Script
 * Handles translation requests, UI interactions, and translation history.
 */

document.addEventListener("DOMContentLoaded", () => {
    // ===================== DOM REFERENCES =====================
    const sourceLang   = document.getElementById("sourceLang");
    const targetLang   = document.getElementById("targetLang");
    const sourceText   = document.getElementById("sourceText");
    const outputText   = document.getElementById("outputText");
    const charCount    = document.getElementById("charCount");
    const translateBtn = document.getElementById("translateBtn");
    const btnText      = document.querySelector(".translate-btn__text");
    const btnLoading   = document.querySelector(".translate-btn__loading");
    const swapBtn      = document.getElementById("swapBtn");
    const clearBtn     = document.getElementById("clearBtn");
    const copyBtn      = document.getElementById("copyBtn");
    const errorMessage = document.getElementById("errorMessage");
    const errorText    = document.getElementById("errorText");
    const successMessage = document.getElementById("successMessage");
    const successText  = document.getElementById("successText");
    const translationTime = document.getElementById("translationTime");
    const historyList  = document.getElementById("historyList");
    const historyEmpty = document.getElementById("historyEmpty");
    const clearHistoryBtn = document.getElementById("clearHistoryBtn");
    const navToggle    = document.getElementById("navToggle");
    const nav          = document.getElementById("nav");
    const header       = document.getElementById("header");

    const HISTORY_KEY  = "linguabridge_history";
    const MAX_HISTORY  = 20;

    // ===================== NAVIGATION =====================
    navToggle.addEventListener("click", () => {
        nav.classList.toggle("open");
    });

    // Close mobile nav on link click
    document.querySelectorAll(".header__nav-link").forEach(link => {
        link.addEventListener("click", () => {
            nav.classList.remove("open");
        });
    });

    // Header scroll shadow
    window.addEventListener("scroll", () => {
        header.classList.toggle("scrolled", window.scrollY > 10);
    });

    // Active nav link on scroll
    const sections = document.querySelectorAll("section[id]");
    window.addEventListener("scroll", () => {
        const scrollY = window.scrollY + 120;
        sections.forEach(section => {
            const top = section.offsetTop;
            const height = section.offsetHeight;
            const id = section.getAttribute("id");
            const link = document.querySelector(`.header__nav-link[href="#${id}"]`);
            if (link) {
                if (scrollY >= top && scrollY < top + height) {
                    document.querySelectorAll(".header__nav-link").forEach(l => l.classList.remove("active"));
                    link.classList.add("active");
                }
            }
        });
    });

    // ===================== CHARACTER COUNTER =====================
    sourceText.addEventListener("input", () => {
        charCount.textContent = sourceText.value.length;
    });

    // ===================== CLEAR BUTTON =====================
    clearBtn.addEventListener("click", () => {
        sourceText.value = "";
        outputText.value = "";
        charCount.textContent = "0";
        translationTime.textContent = "";
        hideMessages();
    });

    // ===================== SWAP LANGUAGES =====================
    swapBtn.addEventListener("click", () => {
        const srcVal = sourceLang.value;
        const tgtVal = targetLang.value;

        // Cannot swap if source is "auto"
        if (srcVal === "auto") {
            showError("Cannot swap when source language is set to 'Detect Language'.");
            return;
        }

        sourceLang.value = tgtVal;
        targetLang.value = srcVal;

        // Also swap text if output has content
        if (outputText.value.trim()) {
            const temp = sourceText.value;
            sourceText.value = outputText.value;
            outputText.value = temp;
            charCount.textContent = sourceText.value.length;
        }
    });

    // ===================== COPY BUTTON =====================
    copyBtn.addEventListener("click", () => {
        const text = outputText.value.trim();
        if (!text) {
            showError("Nothing to copy. Translate something first.");
            return;
        }

        navigator.clipboard.writeText(text).then(() => {
            showSuccess("Translation copied to clipboard!");
            // Reset after 2 seconds
            setTimeout(() => hideMessages(), 2000);
        }).catch(() => {
            // Fallback for older browsers
            outputText.select();
            document.execCommand("copy");
            showSuccess("Translation copied to clipboard!");
            setTimeout(() => hideMessages(), 2000);
        });
    });

    // ===================== TRANSLATE =====================
    translateBtn.addEventListener("click", handleTranslate);

    // Also translate on Ctrl+Enter
    sourceText.addEventListener("keydown", (e) => {
        if (e.ctrlKey && e.key === "Enter") {
            handleTranslate();
        }
    });

    async function handleTranslate() {
        const text   = sourceText.value.trim();
        const source = sourceLang.value;
        const target = targetLang.value;

        hideMessages();
        translationTime.textContent = "";

        // Validate input
        if (!text) {
            showError("Please enter some text to translate.");
            sourceText.focus();
            return;
        }

        if (source !== "auto" && source === target) {
            showError("Source and target languages are the same. Please select different languages.");
            return;
        }

        // Show loading state
        setLoading(true);

        const startTime = performance.now();

        try {
            const response = await fetch("/api/translate", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ text, source, target })
            });

            const data = await response.json();
            const elapsed = ((performance.now() - startTime) / 1000).toFixed(2);

            if (data.success) {
                outputText.value = data.translated_text;
                translationTime.textContent = `⚡ ${elapsed}s`;

                // Save to history
                addToHistory({
                    source,
                    target,
                    sourceText: text,
                    translatedText: data.translated_text,
                    timestamp: new Date().toISOString()
                });
            } else {
                showError(data.error || "Translation failed. Please try again.");
                outputText.value = "";
            }
        } catch (err) {
            console.error("Translation error:", err);
            showError("Could not connect to the translation server. Make sure the Flask backend is running.");
            outputText.value = "";
        } finally {
            setLoading(false);
        }
    }

    // ===================== UI HELPERS =====================
    function setLoading(isLoading) {
        translateBtn.disabled = isLoading;
        btnText.style.display = isLoading ? "none" : "inline-flex";
        btnLoading.style.display = isLoading ? "inline-flex" : "none";
    }

    function showError(msg) {
        hideMessages();
        errorText.textContent = msg;
        errorMessage.style.display = "flex";
    }

    function showSuccess(msg) {
        hideMessages();
        successText.textContent = msg;
        successMessage.style.display = "flex";
    }

    function hideMessages() {
        errorMessage.style.display = "none";
        successMessage.style.display = "none";
    }

    // ===================== LANGUAGE NAME MAP =====================
    const LANG_NAMES = {
        auto: "Auto-Detect",
        en: "English",
        hi: "Hindi",
        es: "Spanish",
        fr: "French",
        de: "German",
        zh: "Chinese",
        ja: "Japanese",
        ko: "Korean",
        ar: "Arabic",
        pt: "Portuguese",
        ru: "Russian",
        bn: "Bengali",
        ta: "Tamil",
        te: "Telugu",
        mr: "Marathi",
        gu: "Gujarati",
        ur: "Urdu"
    };

    // ===================== TRANSLATION HISTORY =====================
    function getHistory() {
        try {
            const data = localStorage.getItem(HISTORY_KEY);
            return data ? JSON.parse(data) : [];
        } catch {
            return [];
        }
    }

    function saveHistory(history) {
        localStorage.setItem(HISTORY_KEY, JSON.stringify(history));
    }

    function addToHistory(entry) {
        const history = getHistory();
        // Add to beginning
        history.unshift(entry);
        // Limit size
        if (history.length > MAX_HISTORY) {
            history.pop();
        }
        saveHistory(history);
        renderHistory();
    }

    function renderHistory() {
        const history = getHistory();

        if (history.length === 0) {
            historyEmpty.style.display = "block";
            // Remove all history items but keep the empty message
            const items = historyList.querySelectorAll(".history-item");
            items.forEach(item => item.remove());
            return;
        }

        historyEmpty.style.display = "none";

        // Clear existing items
        const items = historyList.querySelectorAll(".history-item");
        items.forEach(item => item.remove());

        history.forEach((entry, index) => {
            const srcName = LANG_NAMES[entry.source] || entry.source;
            const tgtName = LANG_NAMES[entry.target] || entry.target;

            const div = document.createElement("div");
            div.classList.add("history-item");
            div.innerHTML = `
                <div class="history-item__langs">${srcName} → ${tgtName}</div>
                <div class="history-item__source">${escapeHtml(entry.sourceText)}</div>
                <div class="history-item__target">→ ${escapeHtml(entry.translatedText)}</div>
            `;

            // Click to re-load into translator
            div.addEventListener("click", () => {
                sourceLang.value = entry.source === "auto" ? "en" : entry.source;
                targetLang.value = entry.target;
                sourceText.value = entry.sourceText;
                outputText.value = entry.translatedText;
                charCount.textContent = entry.sourceText.length;
                // Scroll to translator
                document.getElementById("translator").scrollIntoView({ behavior: "smooth" });
            });

            historyList.appendChild(div);
        });
    }

    clearHistoryBtn.addEventListener("click", () => {
        localStorage.removeItem(HISTORY_KEY);
        renderHistory();
        showSuccess("Translation history cleared.");
        setTimeout(() => hideMessages(), 2000);
    });

    function escapeHtml(str) {
        const div = document.createElement("div");
        div.textContent = str;
        return div.innerHTML;
    }

    // ===================== INITIAL LOAD =====================
    renderHistory();
});

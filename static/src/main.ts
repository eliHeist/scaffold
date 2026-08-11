import './style.css'

import Alpine from "alpinejs";
import mask from '@alpinejs/mask'
import anchor from '@alpinejs/anchor'
import collapse from '@alpinejs/collapse'
import focus from '@alpinejs/focus'

import 'htmx.org';
import "htmx-ext-response-targets";

declare global {
  interface Window {
    Alpine: typeof Alpine;
  }
}

window.Alpine = Alpine
// Alpine.plugin(ajax)
Alpine.plugin(mask)
// Alpine.plugin(intersect)
Alpine.plugin(anchor)
Alpine.plugin(collapse)
// Alpine.plugin(morph)
// Alpine.plugin(persist)
Alpine.plugin(focus)

// handle HTMX requests that swap content with Alpine.js
document.addEventListener('htmx:afterSwap', (event: any) => {
    const xDataElements = event.detail.target.querySelectorAll('[x-data]');
    xDataElements.forEach((element: any) => {
        // If Alpine was already initialized on this element, destroy the existing instance
        if (element.__x) {
            element.__x.cleanups.forEach((cleanup: any) => cleanup()); // Cleanup existing Alpine instance
            delete element.__x; // Remove Alpine's reference
        }
        // Re-initialize Alpine
        Alpine.initTree(element);
    });
});

/**
 * STEAM Lab Inspiration Suite - Moodboard & Shortlist Manager
 * Handles LocalStorage persistence, item notes, moodboard analysis, and brief exports.
 */

class MoodboardManager {
  constructor() {
    this.STORAGE_KEY = 'steam_shortlist_ids_v1';
    this.NOTES_KEY = 'steam_shortlist_notes_v1';
  }

  getSavedIds() {
    try {
      const data = localStorage.getItem(this.STORAGE_KEY);
      return data ? JSON.parse(data) : [];
    } catch (e) {
      console.warn('LocalStorage error:', e);
      return [];
    }
  }

  isSaved(id) {
    const ids = this.getSavedIds();
    return ids.includes(id);
  }

  toggleSave(item) {
    let ids = this.getSavedIds();
    const index = ids.indexOf(item.id);
    let saved = false;

    if (index > -1) {
      ids.splice(index, 1);
      saved = false;
    } else {
      ids.push(item.id);
      saved = true;
    }

    try {
      localStorage.setItem(this.STORAGE_KEY, JSON.stringify(ids));
    } catch (e) {
      console.warn('LocalStorage save error:', e);
    }

    return saved;
  }

  getNotes(id) {
    try {
      const allNotes = JSON.parse(localStorage.getItem(this.NOTES_KEY) || '{}');
      return allNotes[id] || '';
    } catch (e) {
      return '';
    }
  }

  saveNotes(id, noteText) {
    try {
      const allNotes = JSON.parse(localStorage.getItem(this.NOTES_KEY) || '{}');
      if (noteText.trim()) {
        allNotes[id] = noteText.trim();
      } else {
        delete allNotes[id];
      }
      localStorage.setItem(this.NOTES_KEY, JSON.stringify(allNotes));
    } catch (e) {
      console.warn('Notes save error:', e);
    }
  }

  clearAll() {
    localStorage.removeItem(this.STORAGE_KEY);
    localStorage.removeItem(this.NOTES_KEY);
  }

  getSavedItems(catalog) {
    const ids = this.getSavedIds();
    return catalog.filter(item => ids.includes(item.id));
  }

  /**
   * Generates a comprehensive, clean Markdown design brief for export.
   */
  generateMarkdownBrief(savedItems, schoolName = 'Elementary STEAM Lab') {
    const dateStr = new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
    
    let md = `# ${schoolName} - STEAM Lab Design Brief & Moodboard\n`;
    md += `*Curated Inspiration Report generated on ${dateStr}*\n\n`;
    md += `## 🌟 Executive Summary\n`;
    md += `This design brief contains **${savedItems.length} shortlisted logos and artworks** selected for the ${schoolName} makerspace with a guiding focus on **Awe & Wonder**.\n\n`;
    
    // Categorize
    const logos = savedItems.filter(i => i.type === 'logo');
    const artworks = savedItems.filter(i => i.type === 'artwork');
    
    md += `### Breakdown:\n`;
    md += `- **STEAM Logos & Badges**: ${logos.length}\n`;
    md += `- **Murals & Artworks**: ${artworks.length}\n\n`;

    // Collective Color Palette
    const allHexes = [...new Set(savedItems.flatMap(i => i.color_palette || []))].slice(0, 8);
    if (allHexes.length > 0) {
      md += `### 🎨 Recommended Color Palette Swatches:\n`;
      md += allHexes.map(hex => `- \`${hex}\``).join('  ') + `\n\n`;
    }

    md += `---\n\n## 🏷️ Shortlisted Items & Design Analysis\n\n`;

    savedItems.forEach((item, idx) => {
      const userNote = this.getNotes(item.id);
      md += `### ${idx + 1}. [${item.type.toUpperCase()}] ${item.title}\n`;
      md += `- **Category**: ${item.category}\n`;
      md += `- **Grade Appeal**: ${item.grade_appeal}\n`;
      md += `- **Key Motifs**: ${(item.key_motifs || []).join(', ')}\n`;
      md += `- **Why It Inspires Wonder**: ${item.awe_factor}\n`;
      md += `- **Elementary Design Takeaway**: ${item.design_takeaways}\n`;
      if (userNote) {
        md += `- **Teacher's Notes**: *"${userNote}"*\n`;
      }
      md += `- **Source / Credit**: [${item.source_name}](${item.source_url})\n\n`;
    });

    md += `---\n*Generated with STEAM Lab Inspiration Hub*\n`;
    return md;
  }

  /**
   * Generates a printable HTML preview.
   */
  generateHTMLBrief(savedItems, schoolName = 'Elementary STEAM Lab') {
    const dateStr = new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
    const allHexes = [...new Set(savedItems.flatMap(i => i.color_palette || []))].slice(0, 10);

    let html = `
      <div class="brief-report-body" style="color: inherit; line-height: 1.6;">
        <h1 style="font-size: 1.8rem; margin-bottom: 0.25rem;">${schoolName} - Design Brief</h1>
        <p style="color: var(--text-muted); font-size: 0.9rem; margin-bottom: 1.5rem;">Curated Inspiration &amp; Aesthetic Direction • ${dateStr}</p>
        
        <div style="background: var(--bg-surface-elevated); padding: 1.25rem; border-radius: 12px; margin-bottom: 2rem;">
          <h3 style="font-size: 1.1rem; margin-bottom: 0.5rem;">⭐ Shortlist Overview (${savedItems.length} Items)</h3>
          <p style="font-size: 0.92rem; color: var(--text-secondary); margin-bottom: 1rem;">
            A curated moodboard designed to guide signage, lab coats, hallway murals, and visual branding with an emphasis on <strong>Awe &amp; Wonder</strong>.
          </p>
          
          <div style="display: flex; gap: 8px; flex-wrap: wrap; align-items: center;">
            <span style="font-size: 0.8rem; font-weight: 700; color: var(--text-muted);">TOP COLOR SWATCHES:</span>
            ${allHexes.map(hex => `
              <div style="display: inline-flex; align-items: center; gap: 4px; background: var(--bg-main); padding: 3px 8px; border-radius: 6px; font-family: monospace; font-size: 0.8rem;">
                <span style="display: inline-block; width: 14px; height: 14px; border-radius: 3px; background: ${hex}; border: 1px solid rgba(255,255,255,0.2);"></span>
                <span>${hex}</span>
              </div>
            `).join('')}
          </div>
        </div>

        <h3 style="font-size: 1.3rem; margin-bottom: 1rem;">📋 Selected Concepts</h3>
        <div style="display: flex; flex-direction: column; gap: 1.5rem;">
          ${savedItems.map((item, idx) => {
            const userNote = this.getNotes(item.id);
            return `
              <div style="display: grid; grid-template-columns: 140px 1fr; gap: 1.25rem; background: var(--bg-surface); padding: 1.25rem; border-radius: 12px; border: 1px solid var(--border-subtle);">
                <div style="background: var(--bg-main); border-radius: 8px; overflow: hidden; display: flex; align-items: center; justify-content: center; height: 140px;">
                  <img src="${item.image_url}" alt="${item.title}" style="max-width: 100%; max-height: 100%; object-fit: contain;">
                </div>
                <div>
                  <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px;">
                    <span style="font-size: 0.7rem; font-weight: 700; padding: 2px 6px; border-radius: 4px; background: var(--bg-surface-elevated); color: var(--color-cyan);">${item.type.toUpperCase()}</span>
                    <span style="font-size: 0.75rem; color: var(--text-muted);">${item.category} • ${item.grade_appeal}</span>
                  </div>
                  <h4 style="font-size: 1.1rem; margin-bottom: 6px;">${idx + 1}. ${item.title}</h4>
                  <p style="font-size: 0.88rem; color: var(--text-secondary); margin-bottom: 6px;"><strong>Awe Factor:</strong> ${item.awe_factor}</p>
                  <p style="font-size: 0.88rem; color: var(--color-cyan); margin-bottom: 6px;"><strong>Design Tip:</strong> ${item.design_takeaways}</p>
                  ${userNote ? `<div style="background: rgba(255, 183, 3, 0.1); border-left: 3px solid var(--color-yellow); padding: 6px 10px; border-radius: 4px; font-size: 0.85rem; margin-top: 6px;"><strong>Teacher's Note:</strong> ${userNote}</div>` : ''}
                </div>
              </div>
            `;
          }).join('')}
        </div>
      </div>
    `;

    return html;
  }
}

// Global instance
window.moodboardManager = new MoodboardManager();

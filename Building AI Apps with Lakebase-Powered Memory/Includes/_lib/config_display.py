# Includes/_lib/config_display.py
"""HTML "Configuration Values" table for the end of Classroom Setup.

Pattern shared across the Lakebase curriculum so every course's Classroom
Setup ends with a single, consistent summary table instead of scattered
print() statements.

Visual contract (approved palette only):
    - Header bar: solid #1B3139 with white "Configuration Values" title.
    - Two columns: "Information" (bold label suffixed with ":") and "Value".
    - Values are HTML-safe and can include <a> links.
    - Optional "Copy" buttons appear per-row for values a learner is likely
      to paste into an external tool (host, project, user, table names).

Usage in a Classroom Setup notebook:

    from Includes import display_config_values

    display_config_values([
        ("Catalog",         f'<a href="/explore/data/{cat}" target="_blank">{cat}</a>'),
        ("Lakebase project", project, True),   # True -> copy button uses the value
        ("App name",         app_name, True),
    ])

The third tuple element controls the copy button:
    - True               -> button copies the value's text
    - "<custom string>"  -> button copies that exact string
    - omitted / False    -> no button
"""


def display_config_values(config_values, copy_values=False):
    """Render a list of (label, value[, copy_value]) tuples as an HTML
    Configuration Values table. `displayHTML` is provided by the Databricks
    notebook runtime."""
    rows = ""
    for name, value, *rest in config_values:
        copy_value = rest[0] if rest else (copy_values or "")
        copy_btn = ""
        copy_attr = ""
        if copy_value:
            if isinstance(copy_value, str):
                copy_attr = f'data-copy="{copy_value}"'
            copy_btn = """
                <button type="button" onclick="copyFromSibling(this)"
                    style="margin-left:auto;padding:2px 10px;border:1px solid #C4CCD6;border-radius:4px;background:#F9F7F4;cursor:pointer;font-size:13px;flex:0 0 auto;min-width:68px;text-align:center;box-sizing:border-box;">
                    Copy
                </button>"""

        rows += f"""
        <tr>
          <td style="padding:6px 12px;white-space:nowrap;border-bottom:1px solid #DCE0E2;font-weight:600;vertical-align:top;">{name}:</td>
          <td style="padding:6px 12px;border-bottom:1px solid #DCE0E2">
            <div style="display:flex; align-items:center; gap:12px;">
                <span class="copy-source" {copy_attr} style="display:inline-block;padding:4px 8px;font-size:15px;min-width:0;">{value}</span>
                {copy_btn}
            </div>
          </td>
        </tr>"""

    html = """
    <div style="font-family:system-ui,-apple-system,sans-serif;max-width:1100px;margin:12px 0;border:1px solid #DCE0E2;border-radius:8px;overflow:hidden">
      <div style="background:#1B3139;color:#fff;padding:10px 16px;font-size:16px;font-weight:600">Configuration Values</div>
      <table style="width:100%;border-collapse:collapse;font-size:15px">
        <tr style="background:#EEEDE9">
          <th style="padding:6px 12px;text-align:left;border-bottom:1px solid #DCE0E2">Information</th>
          <th style="padding:6px 12px;text-align:left;border-bottom:1px solid #DCE0E2">Value</th>
        </tr>""" + rows + """
      </table>
    </div>
    <script>
        if (!window.copyFromSibling) {
            window.copyFromSibling = function(btn) {
                var source = btn.parentElement.querySelector('.copy-source');
                if (!source) return;
                var text = source.dataset.copy || source.innerText;
                var t = document.createElement('textarea');
                t.value = text;
                t.style.position = 'fixed';
                t.style.opacity = '0';
                t.style.pointerEvents = 'none';
                document.body.appendChild(t);
                t.select();
                document.execCommand('copy');
                document.body.removeChild(t);
                var original = btn.textContent;
                btn.textContent = 'Copied!';
                setTimeout(function() { btn.textContent = original; }, 1500);
            };
        }
    </script>"""

    # `displayHTML` is a Databricks notebook global injected into the main
    # module's namespace, not into builtins. Reach for it via sys.modules
    # first; fall back to IPython's display(HTML(...)) if it isn't there.
    import sys
    db_displayHTML = getattr(sys.modules.get("__main__"), "displayHTML", None)
    if db_displayHTML is not None:
        db_displayHTML(html)
        return
    try:
        from IPython.display import HTML, display
        display(HTML(html))
    except ImportError:
        print(html)

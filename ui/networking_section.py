import html
import re

import streamlit as st
import streamlit.components.v1 as components


def _safe_dom_id(value: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9_-]", "-", value)
    return cleaned or "outreach-message"


def _render_message_editor(message: str, field_id: str):
    escaped_message = html.escape(message)
    dom_id = _safe_dom_id(field_id)

    components.html(
        f"""
        <div style="font-family: sans-serif;">
          <textarea id="{dom_id}" style="
            width: 100%;
            height: 100px;
            padding: 0.5rem;
            border: 1px solid #ccc;
            border-radius: 0.4rem;
            font-size: 0.9rem;
            resize: vertical;
            box-sizing: border-box;
          ">{escaped_message}</textarea>
          <button id="{dom_id}-copy" type="button" style="
            margin-top: 0.5rem;
            padding: 0.45rem 0.9rem;
            border: 1px solid #ccc;
            border-radius: 0.4rem;
            background: #f0f2f6;
            cursor: pointer;
            font-size: 0.9rem;
          ">Copy message</button>
        </div>
        <script>
          (function() {{
            const area = document.getElementById("{dom_id}");
            const btn = document.getElementById("{dom_id}-copy");

            btn.addEventListener("click", async function() {{
              const text = area.value;
              try {{
                await navigator.clipboard.writeText(text);
              }} catch (err) {{
                area.focus();
                area.select();
                document.execCommand("copy");
              }}
              btn.textContent = "Copied!";
              setTimeout(function() {{
                btn.textContent = "Copy message";
              }}, 2000);
            }});
          }})();
        </script>
        """,
        height=155,
    )


def render_networking_result(result, key_prefix=""):

    st.write("LinkedIn contacts")

    if result.people:
        for idx, person in enumerate(result.people):
            name = person.name or "LinkedIn profile"
            label = person.target_type or person.title
            header = f"{name} — {label}" if label else name

            with st.expander(header, expanded=False):
                st.markdown(f"[Open LinkedIn profile]({person.linkedin_url})")
                if person.snippet:
                    st.caption(person.snippet)

                message = person.outreach_message or ""
                _render_message_editor(
                    message,
                    field_id=f"outreach-msg-{key_prefix}-{idx}",
                )
        return

    if not result.discovery_available:
        st.caption(
            "Add SERPAPI_KEY to automatically find public LinkedIn profiles."
        )
    elif result.discovery_error:
        st.caption("Public profile search hit an error.")
    else:
        st.caption("No public LinkedIn profiles were found for this job.")

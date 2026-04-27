import streamlit as st
import streamlit.components.v1 as components
from parser_logic import extract_relationships
from visualizer import generate_mermaid_chart

st.set_page_config(page_title="Archeology Engine", layout="wide")

st.title("Software Archeology Engine")

uploaded_file = st.file_uploader("Upload Java Legacy Monolith", type="java")

if uploaded_file:
    code = uploaded_file.read().decode("utf-8")
    
    try:
        rels = extract_relationships(code)
        
        if not rels:
            st.warning("No relationships found. Try a file where one class calls another!")
        else:
            st.success(f"Extracted {len(rels)} relationships!")
            
            # Create two columns: Metrics and Map
            col1, col2 = st.columns([1, 3])
            
            with col1:
                st.metric("Total Calls", len(rels))
                if st.button("Show Raw Data"):
                    st.write(rels)

            with col2:
                mermaid_string = generate_mermaid_chart(rels)
                
                # Enhanced Mermaid HTML wrapper
                html_code = f"""
                <div id="mermaid-container" style="background-color: white; padding: 20px;">
                    <script type="module">
                        import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
                        mermaid.initialize({{ startOnLoad: true, theme: 'neutral' }});
                    </script>
                    <pre class="mermaid">
                        {mermaid_string}
                    </pre>
                </div>
                """
                components.html(html_code, height=800, scrolling=True)
                
    except Exception as e:
        st.error(f"Error parsing file: {e}")
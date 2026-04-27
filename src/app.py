import streamlit as st
import streamlit.components.v1 as components
import os
import zipfile
import io

from parser_logic import parse_project
from analyzer import build_code_graph, build_method_graph, find_god_objects, find_spaghetti_cycles, cluster_microservices, find_dead_code
from visualizer import generate_mermaid_chart, generate_mermaid_sequence
from cleaner import remove_dead_code
from pdf_generator import generate_pdf_report

st.set_page_config(page_title="Archeology Engine", layout="wide")
st.title("Software Archeology Refactoring Engine")

uploaded_files = st.file_uploader("Upload Java Legacy Monoliths (.java files)", type="java", accept_multiple_files=True)

def render_mermaid(mermaid_string):
    html_code = f"""
    <div id="mermaid-container" style="background-color: white; padding: 20px;">
        <script type="module">
            import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
            mermaid.initialize({{ 
                startOnLoad: true, 
                theme: 'neutral',
                securityLevel: 'loose',
                maxTextSize: 900000,
                flowchart: {{ useMaxWidth: false }}
            }});
        </script>
        <pre class="mermaid">
{mermaid_string.strip()}
        </pre>
    </div>
    """
    components.html(html_code, height=600, scrolling=True)

if uploaded_files:
    projects_dict = {}
    for f in uploaded_files:
        code = f.read().decode("utf-8")
        projects_dict[f.name] = code

    with st.spinner('Excavating CodeBase...'):
        rels, class_stats, lines_info = parse_project(projects_dict)
        
        G_class = build_code_graph(rels)
        G_method = build_method_graph(rels)
        
        god_objects = find_god_objects(G_class, class_stats)
        spaghetti = find_spaghetti_cycles(G_class)
        microservices = cluster_microservices(G_class)
        dead_code = find_dead_code(G_method, class_stats)

    st.success(f"Analysis Complete! Extracted {len(rels)} relationships across {len(class_stats)} classes.")

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Dashboard", 
        "Interactive Map", 
        "God Objects & Spaghetti", 
        "Modernization Roadmap", 
        "Clean Code & Report"
    ])

    with tab1:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Classes", len(class_stats))
        col2.metric("Method Calls", len(rels))
        col3.metric("God Objects", len(god_objects))
        col4.metric("Dead Methods", len(dead_code))
        
        st.subheader("Extracted Relationships Data")
        if st.checkbox("Show Raw Call Graph Data"):
            st.write(rels)

    with tab2:
        st.subheader("Architectural Dependency Map")
        if len(rels) > 0:
            mermaid_str = generate_mermaid_chart(rels)
            render_mermaid(mermaid_str)
        else:
            st.warning("No inter-class dependencies found.")
            
    with tab3:
        st.subheader("God Objects Detected")
        if god_objects:
            st.write(god_objects)
        else:
            st.success("No God Objects detected!")
            
        st.subheader("Spaghetti Cycles")
        if spaghetti:
            for i, cyc in enumerate(spaghetti):
                st.error(f"Cycle {i+1}: {' -> '.join(cyc)} -> {cyc[0]}")
        else:
            st.success("No Cycles detected!")
            
    with tab4:
        st.subheader("Microservice Grouping (Coupling Reduction)")
        for i, ms in enumerate(microservices):
            st.info(f"Microservice Candidate {i+1}: {ms}")
            
        st.subheader("Sample Execution Flow (Sequence Diagram)")
        seq_str = generate_mermaid_sequence(rels)
        render_mermaid(seq_str)
        
    with tab5:
        st.subheader("Archeology Report")
        out_pdf = generate_pdf_report(class_stats, god_objects, spaghetti, dead_code, microservices)
        with open(out_pdf, "rb") as pdf_file:
            st.download_button(
                label="Download Archeology Report (PDF)",
                data=pdf_file,
                file_name="Archeology_Report.pdf",
                mime="application/pdf"
            )

        st.subheader("Clean Code Export (Ghost-code removed)")
        cleaned_files, removed_count = remove_dead_code(projects_dict, dead_code, lines_info)
        st.write(f"Lines removed: {removed_count}")
        
        if st.button("Generate Clean Code Zip"):
            memory_file = io.BytesIO()
            with zipfile.ZipFile(memory_file, 'w') as zf:
                for fname, content in cleaned_files.items():
                    zf.writestr(fname, content)
            memory_file.seek(0)
            st.download_button(
                label="Download Clean Project (ZIP)",
                data=memory_file,
                file_name="clean_project.zip",
                mime="application/zip"
            )
else:
    st.info("Upload files to begin mapping...")
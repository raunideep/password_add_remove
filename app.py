import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import io

# 1. Page Config (Wide Layout for Embed Optimization)
st.set_page_config(
    page_title="AI Professional Resume & Cover Letter Generator",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Custom CSS to eliminate Streamlit's default padding and white spaces
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        .block-container {
            padding-top: 1.5rem !important;
            padding-bottom: 1.5rem !important;
            padding-left: 2rem !important;
            padding-right: 2rem !important;
            max-width: 100% !important;
        }
        
        .stButton>button {
            width: 100%;
            border-radius: 6px;
            font-weight: 600;
        }
    </style>
""", unsafe_allow_html=True)

# 3. PDF Generation Logic using ReportLab
def generate_pdf(data, doc_type="Resume"):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=letter,
        rightMargin=36, 
        leftMargin=36,
        topMargin=36, 
        bottomMargin=36
    )
    
    styles = getSampleStyleSheet()
    story = []
    
    # Custom Palette Selection based on theme choice
    primary_color = colors.HexColor("#1e3a8a") if data.get('theme') == "Classic Blue" else colors.HexColor("#0f766e")
    
    # Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=24,
        leading=28,
        textColor=primary_color,
        spaceAfter=6
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontSize=11,
        leading=14,
        textColor=colors.HexColor("#4b5563"),
        spaceAfter=15
    )
    
    heading_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontSize=14,
        leading=18,
        textColor=primary_color,
        spaceBefore=12,
        spaceAfter=6,
        borderPadding=(0, 0, 2, 0),
        borderColor=primary_color,
        borderWidth=1
    )
    
    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#1f2937"),
        spaceAfter=6
    )

    # Document Header Content
    story.append(Paragraph(data.get('name', 'Your Name'), title_style))
    contact_info = f"{data.get('email', '')} | {data.get('phone', '')} | {data.get('location', '')}"
    story.append(Paragraph(contact_info, subtitle_style))
    story.append(Spacer(1, 10))

    if doc_type == "Resume":
        # Summary Section
        if data.get('summary'):
            story.append(Paragraph("Professional Summary", heading_style))
            story.append(Paragraph(data.get('summary'), body_style))
            story.append(Spacer(1, 8))

        # Skills Section
        if data.get('skills'):
            story.append(Paragraph("Core Competencies & Skills", heading_style))
            skills_list = [s.strip() for s in data.get('skills', '').split(',')]
            # Format skills into a neat multi-column grid table
            formatted_skills = [[Paragraph(f"• {skill}", body_style) for skill in skills_list[i:i+3]] for i in range(0, len(skills_list), 3)]
            if formatted_skills:
                skills_table = Table(formatted_skills, colWidths=[180, 180, 180])
                skills_table.setStyle(TableStyle([
                    ('VALIGN', (0,0), (-1,-1), 'TOP'),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
                ]))
                story.append(skills_table)
            story.append(Spacer(1, 8))

        # Experience Section
        if data.get('experience'):
            story.append(Paragraph("Professional Experience", heading_style))
            story.append(Paragraph(data.get('experience'), body_style))
            story.append(Spacer(1, 8))

        # Education Section
        if data.get('education'):
            story.append(Paragraph("Education & Credentials", heading_style))
            story.append(Paragraph(data.get('education'), body_style))

    else:
        # Cover Letter Specific Layout
        if data.get('recipient_name'):
            story.append(Paragraph(f"<b>To:</b> {data.get('recipient_name')}", body_style))
        if data.get('company_name'):
            story.append(Paragraph(f"<b>Company:</b> {data.get('company_name')}", body_style))
        story.append(Spacer(1, 10))
        
        story.append(Paragraph("Dear Hiring Manager,", body_style))
        story.append(Spacer(1, 6))
        
        if data.get('cover_body'):
            story.append(Paragraph(data.get('cover_body'), body_style))
            
        story.append(Spacer(1, 15))
        story.append(Paragraph("Sincerely,", body_style))
        story.append(Spacer(1, 4))
        story.append(Paragraph(data.get('name', 'Your Name'), body_style))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()

# 4. Main Streamlit User Interface Layout
def main():
    st.markdown("<h2 style='text-align: center; color: #2563eb;'>AI Professional Resume & Cover Letter Generator</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748b;'>Build, customize, and instantly download print-ready career documents.</p>", unsafe_allow_html=True)
    st.markdown("---")

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.subheader("1. Document Configuration")
        doc_type = st.selectbox("Select Document Type", ["Resume", "Cover Letter"])
        theme_style = st.selectbox("Select Template Theme", ["Classic Blue", "Modern Teal"])
        
        st.markdown("### 2. Personal Information")
        name = st.text_input("Full Name", "Alex Morgan")
        email = st.text_input("Email Address", "alex.morgan@email.com")
        phone = st.text_input("Phone Number", "+1 (555) 019-2834")
        location = st.text_input("Location", "San Francisco, CA")

        data = {
            "name": name,
            "email": email,
            "phone": phone,
            "location": location,
            "theme": theme_style
        }

        if doc_type == "Resume":
            st.markdown("### 3. Professional Background")
            data["summary"] = st.text_area("Professional Summary", "Results-driven professional with extensive expertise in cross-functional project management, technical development, and high-performance system designs.")
            data["skills"] = st.text_area("Skills (Comma-separated)", "Python, Streamlit, Project Management, Data Analysis, UI/UX Design, Problem Solving, Agile Methodologies")
            data["experience"] = st.text_area("Work Experience Details", "Senior Consultant | TechCorp Inc. (2022 - Present)\n• Spearheaded scalable software implementation strategies.\n• Optimized database query performance by 40%.")
            data["education"] = st.text_area("Education", "B.S. in Computer Science | University of California (2018 - 2022)")
        else:
            st.markdown("### 3. Cover Letter Details")
            data["recipient_name"] = st.text_input("Hiring Manager / Recipient Name", "Jane Doe")
            data["company_name"] = st.text_input("Company Name", "InnoTech Solutions")
            data["cover_body"] = st.text_area("Cover Letter Body Paragraphs", "I am writing to express my strong interest in the open position at your esteemed organization. With my robust background in technical architecture and professional design execution, I am confident in my ability to bring immediate value to your team.")

    with col2:
        st.subheader("Live Document Preview & Export")
        st.info("Your custom-formatted document is ready for generation below.")
        
        # Preview Card Representation
        with st.container(border=True):
            st.markdown(f"### **{name}**")
            st.caption(f"{email} | {phone} | {location}")
            st.divider()
            
            if doc_type == "Resume":
                st.markdown("#### **Professional Summary**")
                st.write(data.get("summary", ""))
                st.markdown("#### **Core Competencies**")
                st.write(data.get("skills", ""))
                st.markdown("#### **Experience**")
                st.write(data.get("experience", ""))
            else:
                st.markdown(f"**To:** {data.get('recipient_name')} ({data.get('company_name')})")
                st.write("Dear Hiring Manager,")
                st.write(data.get("cover_body", ""))
                st.write("Sincerely,")
                st.write(name)

        st.markdown("<br>", unsafe_allow_html=True)
        
        # PDF Generation Button
        pdf_bytes = generate_pdf(data, doc_type)
        st.download_button(
            label=f"📥 Download {doc_type} as PDF",
            data=pdf_bytes,
            file_name=f"{name.replace(' ', '_')}_{doc_type}.pdf",
            mime="application/pdf",
            use_container_width=True
        )

if __name__ == '__main__':
    main()
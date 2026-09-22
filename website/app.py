import streamlit as st
import textwrap
import os
import sys
import json
import subprocess
import tempfile

# ==========================================
# HTML Rendering Helper
# ==========================================

def render_html(content):
    st.html(
        textwrap.dedent(content)
    )


# ==========================================
# Page Configuration
# ==========================================

st.set_page_config(
    page_title="CounterShield AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ==========================================
# Custom CSS
# ==========================================

st.markdown(
    """
<style>

.stApp {
    background-color: #050b16;

    background-image:
        /* Soft blue glow - top left */
        radial-gradient(
            circle at 10% 10%,
            rgba(65, 150, 255, 0.20),
            transparent 28%
        ),

        /* Soft purple glow - top right */
        radial-gradient(
            circle at 90% 15%,
            rgba(120, 80, 255, 0.16),
            transparent 25%
        ),

        /* Soft cyan glow - bottom right */
        radial-gradient(
            circle at 80% 85%,
            rgba(0, 200, 255, 0.12),
            transparent 30%
        ),

        /* Very subtle diagonal pattern */
        linear-gradient(
            135deg,
            rgba(255, 255, 255, 0.012) 25%,
            transparent 25%
        ),

        linear-gradient(
            315deg,
            rgba(255, 255, 255, 0.008) 25%,
            transparent 25%
        ),

        /* Very subtle technical grid */
        linear-gradient(
            90deg,
            rgba(255, 255, 255, 0.012) 1px,
            transparent 1px
        ),

        linear-gradient(
            0deg,
            rgba(255, 255, 255, 0.012) 1px,
            transparent 1px
        );

    background-size:
        auto,
        auto,
        auto,
        80px 80px,
        80px 80px,
        50px 50px,
        50px 50px;

    background-position:
        center,
        center,
        center,
        center,
        center,
        center,
        center;

    background-attachment: fixed;

    color: white;
}

[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stToolbar"] {
    background: transparent;
}

.block-container {
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

.hero-box {
    position: relative;
    text-align: center;
    padding: 45px 20px 35px 20px;
}

.hero-box::after {
    content: "";

    position: absolute;

    left: 15%;
    right: 15%;

    top: 38%;

    height: 1px;

    background: linear-gradient(
        90deg,
        transparent,
        rgba(77, 210, 255, 0.0),
        rgba(77, 210, 255, 0.65),
        rgba(0, 230, 210, 0.75),
        rgba(77, 210, 255, 0.0),
        transparent
    );

    box-shadow:
        0 0 12px rgba(77, 210, 255, 0.35);

    opacity: 0.35;

    pointer-events: none;

    animation: heroScan 6s ease-in-out infinite;
}

@keyframes heroScan {
    0%, 100% {
        transform: translateY(-55px);
        opacity: 0.15;
    }

    50% {
        transform: translateY(55px);
        opacity: 0.55;
    }
}

/* =========================================================
   AI Circuit Decorations
   ========================================================= */

.hero-circuit {
    position: absolute;
    top: 42%;
    width: 150px;
    height: 70px;
    opacity: 0.55;
    pointer-events: none;
}

.hero-circuit.left {
    left: 0;
}

.hero-circuit.right {
    right: 0;
    transform: scaleX(-1);
}

.circuit-line {
    position: absolute;
    top: 30px;
    left: 10px;
    width: 120px;
    height: 1px;
    background: linear-gradient(
        90deg,
        transparent,
        rgba(77, 190, 255, 0.65)
    );
}

.circuit-vertical {
    position: absolute;
    top: 30px;
    left: 65px;
    width: 1px;
    height: 35px;
    background: rgba(77, 190, 255, 0.55);
}

.circuit-node {
    position: absolute;
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #55dfff;

    box-shadow:
        0 0 8px rgba(85, 223, 255, 0.9),
        0 0 18px rgba(85, 223, 255, 0.35);
}

.node-one {
    top: 27px;
    left: 5px;
}

.node-two {
    top: 27px;
    left: 117px;
}

.node-three {
    top: 61px;
    left: 62px;
}

/* =========================================================
   Floating AI Particles
   ========================================================= */

.ai-particle {
    position: absolute;

    width: 5px;
    height: 5px;

    border-radius: 50%;

    background: #55dfff;

    box-shadow:
        0 0 8px rgba(85, 223, 255, 0.9),
        0 0 18px rgba(85, 223, 255, 0.35);

    pointer-events: none;

    animation: aiParticleFloat 5s ease-in-out infinite;
}

.ai-particle.one {
    top: 18%;
    left: 18%;
}

.ai-particle.two {
    top: 28%;
    right: 18%;
    animation-delay: 1.5s;
}

.ai-particle.three {
    top: 62%;
    left: 12%;
    animation-delay: 3s;
}

.ai-particle.four {
    top: 68%;
    right: 12%;
    animation-delay: 2s;
}

@keyframes aiParticleFloat {
    0%, 100% {
        transform: translateY(0);
        opacity: 0.35;
    }

    50% {
        transform: translateY(-10px);
        opacity: 0.85;
    }
}

.hero-icon {
    font-size: 64px;
    margin-bottom: 8px;
    filter: drop-shadow(0 0 14px rgba(77, 166, 255, 0.45));
}

.hero-title {
    font-size: 52px;
    font-weight: 850;
    color: #ffffff;
    margin: 0;
    letter-spacing: -1px;
    text-shadow: 0 0 24px rgba(77, 166, 255, 0.20);
}

.hero-subtitle {
    font-size: 21px;
    font-weight: 600;
    color: #72c4ff;
    margin-top: 10px;
    letter-spacing: 0.3px;
}

.hero-description {
    max-width: 760px;
    margin: 17px auto 0 auto;
    color: #aab8c8;
    font-size: 16px;
    line-height: 1.7;
}

.ai-status {
    display: inline-flex;
    align-items: center;
    gap: 8px;

    margin-top: 18px;
    padding: 7px 15px;

    border-radius: 999px;

    background: rgba(0, 200, 180, 0.08);
    border: 1px solid rgba(0, 220, 200, 0.25);

    color: #9be9df;

    font-size: 12px;
    font-weight: 700;

    letter-spacing: 0.8px;

    box-shadow:
        0 0 18px rgba(0, 220, 200, 0.06);
}

.ai-status-dot {
    width: 7px;
    height: 7px;

    border-radius: 50%;

    background: #55e6d1;

    box-shadow:
        0 0 8px rgba(85, 230, 209, 0.9);
}

.section-heading {
    color: #ffffff;
    font-size: 27px;
    font-weight: 800;

    margin-top: 15px;
    margin-bottom: 20px;

    letter-spacing: -0.2px;

    text-shadow:
        0 0 16px rgba(77, 166, 255, 0.10);

    position: relative;
}

.section-heading::after {
    content: "";

    display: block;

    width: 46px;
    height: 2px;

    margin-top: 9px;

    border-radius: 2px;

    background: linear-gradient(
        90deg,
        #4da6ff,
        #00d9c6
    );

    box-shadow:
        0 0 8px rgba(77, 166, 255, 0.30);
}

.product-card {
    background: rgba(12, 25, 42, 0.72);
    border: 1px solid rgba(100, 180, 255, 0.22);
    border-radius: 18px;
    padding: 22px 18px;
    text-align: center;
    min-height: 105px;

    box-shadow:
        0 8px 25px rgba(0, 0, 0, 0.20),
        inset 0 1px 0 rgba(255, 255, 255, 0.035);

    transition:
        transform 0.25s ease,
        border-color 0.25s ease,
        box-shadow 0.25s ease;
}

.product-card {
    position: relative;
    overflow: hidden;
}

.product-card::before {
    content: "";

    position: absolute;

    top: 0;
    left: 12%;
    right: 12%;

    height: 1px;

    background: linear-gradient(
        90deg,
        transparent,
        rgba(77, 210, 255, 0.65),
        transparent
    );

    opacity: 0.55;
}

.product-card:hover {
    transform: translateY(-4px);

    border-color: rgba(100, 200, 255, 0.38);

    box-shadow:
        0 14px 32px rgba(0, 0, 0, 0.28),
        0 0 20px rgba(77, 166, 255, 0.08),
        inset 0 1px 0 rgba(255, 255, 255, 0.05);
}

.card-icon {
    font-size: 34px;
    text-align: center;
    margin-top: 4px;
    margin-bottom: 4px;
    filter: drop-shadow(0 0 7px rgba(77, 166, 255, 0.25));
}

.card-title {
    color: #ffffff;
    font-size: 17px;
    font-weight: 700;
    text-align: center;
    margin-top: 8px;
    letter-spacing: 0.2px;
}

.card-description {
    color: #91b4d4;
    font-size: 13px;
    text-align: center;
    margin-top: 6px;
    line-height: 1.5;
}

.upload-card {
    position: relative;
    overflow: hidden;

    background: rgba(255, 255, 255, 0.045);

    border: 1px solid rgba(120, 190, 255, 0.18);

    border-radius: 20px;

    padding: 25px;

    box-shadow:
        0 8px 28px rgba(0, 0, 0, 0.18),
        inset 0 1px 0 rgba(255, 255, 255, 0.035);
}

.upload-card::before {
    content: "";

    position: absolute;

    top: 0;
    left: 15%;
    right: 15%;

    height: 1px;

    background: linear-gradient(
        90deg,
        transparent,
        rgba(77, 210, 255, 0.70),
        rgba(0, 230, 210, 0.70),
        transparent
    );

    box-shadow:
        0 0 12px rgba(77, 210, 255, 0.35);

    opacity: 0.55;
}



.upload-heading {
    color: #ffffff;
    font-size: 20px;
    font-weight: 750;
    text-align: center;

    letter-spacing: 0.2px;

    text-shadow:
        0 0 12px rgba(77, 166, 255, 0.12);
}

.upload-description {
    color: #9db9d1;
    text-align: center;
    font-size: 14px;
    margin-top: 8px;
    line-height: 1.5;
}

.result-card {
    background: rgba(12, 25, 42, 0.78);

    border: 1px solid rgba(100, 180, 255, 0.24);

    border-radius: 20px;

    padding: 30px 25px;

    text-align: center;

    box-shadow:
        0 10px 30px rgba(0, 0, 0, 0.24),
        inset 0 1px 0 rgba(255, 255, 255, 0.04);
}

.result-icon {
    font-size: 48px;
    margin-bottom: 8px;
    filter: drop-shadow(
        0 0 10px rgba(77, 166, 255, 0.30)
    );
}

.result-prediction {
    color: #ffffff;
    font-size: 34px;
    font-weight: 850;
    margin-top: 8px;
    letter-spacing: 0.3px;
}

.result-message {
    color: #91b4d4;
    font-size: 14px;
    margin-top: 10px;
}

.result-card.genuine {
    border-color: rgba(80, 220, 190, 0.30);

    box-shadow:
        0 10px 30px rgba(0, 0, 0, 0.24),
        0 0 22px rgba(80, 220, 190, 0.06);
}

.result-card.counterfeit {
    border-color: rgba(255, 170, 90, 0.30);

    box-shadow:
        0 10px 30px rgba(0, 0, 0, 0.24),
        0 0 22px rgba(255, 170, 90, 0.06);
}

.result-label {
    color: #91a4ba;
    font-size: 13px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.result-value {
    color: white;
    font-size: 32px;
    font-weight: 800;
    margin-top: 8px;
}

.confidence-value {
    color: #72b9ff;
    font-size: 26px;
    font-weight: 700;
}

.explanation-card {
    background: rgba(255, 255, 255, 0.045);
    border-left: 4px solid #4da6ff;
    border-radius: 12px;
    padding: 18px;
    color: #aab8c8;
    line-height: 1.6;
}

.explanation-box {
    background: rgba(20, 35, 55, 0.72);
    border: 1px solid rgba(77, 166, 255, 0.28);
    border-radius: 16px;
    padding: 22px 26px;
    margin: 18px 0 24px 0;
    box-shadow: 0 8px 28px rgba(0, 0, 0, 0.22);
    backdrop-filter: blur(8px);
}

.explanation-title {
    color: #ffffff;
    font-size: 17px;
    font-weight: 750;
    letter-spacing: 0.2px;
    margin-bottom: 8px;
}

.explanation-text {
    color: #a9bfd4;
    font-size: 14px;
    line-height: 1.6;
}

.stButton > button {
    width: 100%;
    min-height: 52px;

    border-radius: 14px;

    background: linear-gradient(
        135deg,
        #1877f2,
        #00a6ff
    ) !important;

    border: 1px solid rgba(120, 210, 255, 0.45) !important;

    color: #ffffff !important;

    font-size: 16px;
    font-weight: 750;

    letter-spacing: 0.3px;

    box-shadow:
        0 8px 22px rgba(0, 120, 255, 0.22),
        inset 0 1px 0 rgba(255, 255, 255, 0.20);

    transition:
        transform 0.2s ease,
        box-shadow 0.2s ease,
        filter 0.2s ease;
}

.stButton > button:hover {
    filter: brightness(1.08);

    transform: translateY(-2px);

    box-shadow:
        0 12px 28px rgba(0, 150, 255, 0.32),
        0 0 18px rgba(0, 180, 255, 0.18);
}

.stButton > button:active {
    transform: translateY(0px);
}

[data-testid="stImage"] {
    border-radius: 16px;
    overflow: hidden;

    box-shadow:
        0 10px 30px rgba(0, 0, 0, 0.25),
        0 0 18px rgba(77, 166, 255, 0.06);
}

/* Grad-CAM image caption */
[data-testid="stImage"] img {
    border-radius: 14px;
}

hr {
    border-color: rgba(255, 255, 255, 0.10);
    margin-top: 35px;
    margin-bottom: 35px;
}

.footer {
    text-align: center;
    color: #718197;
    font-size: 13px;
    line-height: 1.7;
    padding: 25px 10px;
}

/* =========================================================
   CounterShield Upload Area
   ========================================================= */

[data-testid="stFileUploader"] {
    background: rgba(12, 25, 42, 0.72);
    border: 1px solid rgba(100, 180, 255, 0.22);
    border-radius: 16px;
    padding: 8px;
}

[data-testid="stFileUploaderDropzone"] {
    background: rgba(8, 20, 35, 0.70) !important;
    border: 1px dashed rgba(100, 190, 255, 0.30) !important;
    border-radius: 12px !important;
}

[data-testid="stFileUploaderDropzone"] button {
    background: rgba(77, 166, 255, 0.12) !important;
    border: 1px solid rgba(77, 166, 255, 0.30) !important;
    color: #ffffff !important;
}

[data-testid="stFileUploaderDropzone"] button * {
    color: #ffffff !important;
}

[data-testid="stFileUploaderDropzone"] small,
[data-testid="stFileUploaderDropzone"] p,
[data-testid="stFileUploaderDropzone"] span {
    color: #ffffff !important;
}

</style>
""",
    unsafe_allow_html=True
)


# ==========================================
# Hero Section
# ==========================================

render_html(
    """
    <div class="hero-box">
        <div class="ai-particle one"></div>
        <div class="ai-particle two"></div>
        <div class="ai-particle three"></div>
        <div class="ai-particle four"></div>

        <div class="hero-circuit left">
            <div class="circuit-line"></div>
            <div class="circuit-vertical"></div>

            <div class="circuit-node node-one"></div>
            <div class="circuit-node node-two"></div>
            <div class="circuit-node node-three"></div>
        </div>

        <div class="hero-circuit right">
            <div class="circuit-line"></div>
            <div class="circuit-vertical"></div>

            <div class="circuit-node node-one"></div>
            <div class="circuit-node node-two"></div>
            <div class="circuit-node node-three"></div>
        </div>

        <div class="hero-icon">🛡️</div>

        <div class="hero-title">
            CounterShield AI
        </div>

        <div class="hero-subtitle">
            Intelligent Product Authenticity Analysis
        </div>

        <div class="ai-status">
            <span class="ai-status-dot"></span>
              Product Classification Module • XAI ENABLED 
        </div>

        <div class="hero-description">
            An AI-powered computer vision system designed to
            classify supported packaged products as
            <b>Genuine</b> or <b>Counterfeit</b>.
        </div>

    </div>
    """
)


# ==========================================
# How CounterShield Works
# ==========================================

render_html(
    """
    <div class="section-heading">
        How CounterShield Works
    </div>
    """
)

step1, step2, step3, step4 = st.columns(4)

with step1:
    render_html(
        """
        <div class="product-card">

            <div class="card-icon">📤</div>

            <div class="card-title">
                Upload
            </div>

            <div class="card-description">
                Choose a product image
            </div>

        </div>
        """
    )

with step2:
    render_html(
        """
        <div class="product-card">

            <div class="card-icon">🔍</div>

            <div class="card-title">
                Analyze
            </div>

            <div class="card-description">
                AI processes the image
            </div>

        </div>
        """
    )

with step3:
    render_html(
        """
        <div class="product-card">

            <div class="card-icon">🧠</div>

            <div class="card-title">
                Classify
            </div>

            <div class="card-description">
                Genuine or Counterfeit
            </div>

        </div>
        """
    )

with step4:
    render_html(
        """
        <div class="product-card">

            <div class="card-icon">🔥</div>

            <div class="card-title">
                Explain
            </div>

            <div class="card-description">
                Grad-CAM visualization
            </div>

        </div>
        """
    )


st.divider()


# ==========================================
# Supported Products
# ==========================================

render_html(
    """
    <div class="section-heading">
        Supported Products
    </div>
    """
)

product1, product2, product3, product4 = st.columns(4)

with product1:
    render_html(
        """
        <div class="product-card">

            <div class="card-icon">🧈</div>

            <div class="card-title">
                Amul Butter
            </div>

        </div>
        """
    )

with product2:
    render_html(
        """
        <div class="product-card">

            <div class="card-icon">💧</div>

            <div class="card-title">
                Bisleri
            </div>

        </div>
        """
    )

with product3:
    render_html(
        """
        <div class="product-card">

            <div class="card-icon">🍪</div>

            <div class="card-title">
                Parle-G
            </div>

        </div>
        """
    )

with product4:
    render_html(
        """
        <div class="product-card">

            <div class="card-icon">🍪</div>

            <div class="card-title">
                Parle-G Gold
            </div>

        </div>
        """
    )


st.divider()


# ==========================================
# Upload Section
# ==========================================

render_html(
    """
    <div class="section-heading">
        Analyze Your Product
    </div>
    """
)

render_html(
    """
    <div class="upload-card">

        <div class="upload-heading">
            📷 Upload a Product Image
        </div>

        <div class="upload-description">
            Supported formats: JPG, JPEG, PNG
        </div>

    </div>
    """
)

# ============================================================
# Product Analysis
# ============================================================

uploaded_file = st.file_uploader(
    "Choose a product image",
    type=["jpg", "jpeg", "png"],
    label_visibility="collapsed"
)

if uploaded_file is not None:

    # Display uploaded image
    st.image(
        uploaded_file,
        caption="Uploaded Product Image",
        width=500
    )

    st.write("")

    # Analyze button
    if st.button(
        "🔍 Analyze Product",
        use_container_width=True
    ):

        with st.spinner("CounterShield AI is analyzing the product..."):

            temp_path = None

            try:
                # ------------------------------------------------
                # Save uploaded image temporarily
                # ------------------------------------------------
                file_extension = os.path.splitext(
                    uploaded_file.name
                )[1].lower()

                if file_extension not in [".jpg", ".jpeg", ".png"]:
                    file_extension = ".jpg"

                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=file_extension
                ) as temp_file:

                    temp_file.write(
                        uploaded_file.getbuffer()
                    )

                    temp_path = temp_file.name

                # ------------------------------------------------
                # Run EfficientNetB0 + Grad-CAM
                # ------------------------------------------------
                result = subprocess.run(
                    [
                        sys.executable,
                        "gradcam_test.py",
                        temp_path
                    ],
                    capture_output=True,
                    text=True
                )

                # ------------------------------------------------
                # Check prediction script
                # ------------------------------------------------
                if result.returncode != 0:

                    st.error(
                        "The AI analysis could not be completed."
                    )

                    with st.expander("Technical Details"):
                        st.code(
                            result.stderr or result.stdout
                        )

                else:

                    # ------------------------------------------------
                    # Read structured prediction result
                    # ------------------------------------------------
                    result_path = (
                        "model/efficientnetb0/"
                        "prediction_result.json"
                    )

                    if os.path.exists(result_path):

                        with open(
                            result_path,
                            "r",
                            encoding="utf-8"
                        ) as result_file:

                            prediction_result = json.load(
                                result_file
                            )

                        prediction = prediction_result.get(
                            "prediction",
                            "Unknown"
                        )

                        confidence = float(
                            prediction_result.get(
                                "confidence",
                                0
                            )
                        )

                        gradcam_path = prediction_result.get(
                            "gradcam_path",
                            "model/efficientnetb0/"
                            "gradcam_result.png"
                        )

                        # ------------------------------------------------
                        # Result Section
                        # ------------------------------------------------
                        st.divider()

                        render_html(
                            """
                            <div class="section-heading">
                                Analysis Result
                            </div>
                            """
                        )

                        if prediction == "Genuine":

                            result_class = "genuine"

                            result_icon = "🛡️"

                            result_message = (
                                "The model classified this "
                                "product image as Genuine."
                            )

                        else:

                            result_class = "counterfeit"

                            result_icon = "⚠️"

                            result_message = (
                                "The model classified this "
                                "product image as Counterfeit."
                            )

                        # ------------------------------------------------
                        # Prediction Card
                        # ------------------------------------------------
                        render_html(
                            f"""
                            <div class="result-card {result_class}">

                                <div class="result-icon">
                                    {result_icon}
                                </div>

                                <div class="result-label">
                                    AI Classification
                                </div>

                                <div class="result-prediction">
                                    {prediction}
                                </div>

                                
                                <div class="result-message">
                                    {result_message}
                                </div>

                            </div>
                            """
                        )

                        # ------------------------------------------------
                        # Confidence display
                        # ------------------------------------------------
                        confidence = float(
                            prediction_result.get(
                                "confidence",
                                0
                                )
                            )
                    
                        

                        # ------------------------------------------------
                        # Grad-CAM Explanation
                        # ------------------------------------------------
                        if os.path.exists(gradcam_path):

                            render_html(
                                """
                                <div class="section-heading">
                                    AI Explanation
                                </div>
                                """
                            )

                            render_html(
                                """
                                <div class="explanation-box">

                                    <div class="explanation-title">
                                        🔥 Grad-CAM Visualization
                                    </div>

                                    <div class="explanation-text">
                                        The highlighted regions show
                                        areas of the image that contributed
                                        to the model's classification.
                                    </div>

                                </div>
                                """
                            )

                            st.image(
                                gradcam_path,
                                caption=(
                                    "Grad-CAM: Areas influencing "
                                    "the AI classification"
                                ),
                                width=700
                            )

                        else:

                            st.warning(
                                "Grad-CAM visualization was not found."
                            )

                    else:

                        st.error(
                            "Prediction result file was not generated."
                        )

            except Exception as error:

                st.error(
                    "An unexpected error occurred during analysis."
                )

                with st.expander("Technical Details"):
                    st.exception(error)

            finally:

                # ------------------------------------------------
                # Remove temporary uploaded image
                # ------------------------------------------------
                if temp_path is not None:

                    try:
                        if os.path.exists(temp_path):
                            os.remove(temp_path)

                    except Exception:
                        pass

st.divider()


# ==========================================
# Footer
# ==========================================

render_html(
    """
    <div class="footer">

        <strong>CounterShield AI</strong><br>

        AI-Based Packaged Product Authenticity Classification

        <br><br>

        CounterShield provides image-based AI classification
        and does not constitute physical or legal authentication
        of a product.

    </div>
    """
)
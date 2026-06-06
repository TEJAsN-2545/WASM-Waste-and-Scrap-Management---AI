from ultralytics import YOLO
import streamlit as st
import streamlit.components.v1 as components
import cv2
import settings

def load_model(model_path):
    """
    Loads a YOLO object detection model from the specified model_path.
    """
    model = YOLO(model_path)
    return model


def display_tracker_options():
    display_tracker = st.radio("Display Tracker", ('Yes', 'No'))
    is_display_tracker = True if display_tracker == 'Yes' else False
    if is_display_tracker:
        tracker_type = st.radio("Tracker", ("bytetrack.yaml", "botsort.yaml"))
        return is_display_tracker, tracker_type
    return is_display_tracker, None


def _display_detected_frames(conf, model, st_frame, image, is_display_tracking=None, tracker=None):
    """
    Display the detected objects on a video frame using the YOLOv8 model.
    """
    image = cv2.resize(image, (720, int(720*(9/16))))

    if is_display_tracking:
        res = model.track(image, conf=conf, persist=True, tracker=tracker)
    else:
        res = model.predict(image, conf=conf)

    res_plotted = res[0].plot()
    st_frame.image(res_plotted,
                   caption='Detected Video',
                   channels="BGR",
                   use_column_width=True)


def play_webcam(conf, model):
    """
    Plays a webcam stream. Detects Objects in real-time using the YOLOv8 model.
    """
    source_webcam = settings.WEBCAM_PATH
    is_display_tracker, tracker = display_tracker_options()
    if st.sidebar.button('Detect Trash'):
        try:
            vid_cap = cv2.VideoCapture(source_webcam)
            st_frame = st.empty()
            while (vid_cap.isOpened()):
                success, image = vid_cap.read()
                if success:
                    _display_detected_frames(conf, model, st_frame, image, 
                                           is_display_tracker, tracker)
                else:
                    vid_cap.release()
                    break
        except Exception as e:
            st.sidebar.error("Error loading video: " + str(e))


def generate_3d_model(material_type, custom_prompt):
    """
    Generates and displays a 3D model based on material type and prompt using Three.js
    """
    
    # Define colors and properties for different materials
    material_properties = {
        "Plastic": {"color": "0x3498db", "metalness": 0.3, "roughness": 0.4, "shape": "bottle"},
        "Metal": {"color": "0x95a5a6", "metalness": 0.9, "roughness": 0.1, "shape": "can"},
        "Glass": {"color": "0x27ae60", "metalness": 0.1, "roughness": 0.05, "shape": "bottle"},
        "Paper": {"color": "0xf4d03f", "metalness": 0.0, "roughness": 0.9, "shape": "box"},
        "Cardboard": {"color": "0xd68910", "metalness": 0.0, "roughness": 0.8, "shape": "box"},
        "Biodegradable": {"color": "0x52be80", "metalness": 0.2, "roughness": 0.6, "shape": "sphere"}
    }
    
    props = material_properties.get(material_type, material_properties["Plastic"])
    
    # Create Three.js HTML
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ margin: 0; overflow: hidden; }}
            #info {{
                position: absolute;
                top: 10px;
                left: 10px;
                color: white;
                font-family: Arial;
                background: rgba(0,0,0,0.7);
                padding: 10px;
                border-radius: 5px;
            }}
        </style>
    </head>
    <body>
        <div id="info">
            <strong>Material:</strong> {material_type}<br>
            <strong>Description:</strong> {custom_prompt if custom_prompt else 'Generic ' + material_type + ' item'}<br>
            <em>Drag to rotate • Scroll to zoom</em>
        </div>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
        <script>
            // Scene setup
            const scene = new THREE.Scene();
            scene.background = new THREE.Color(0x1a1a1a);
            
            const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
            const renderer = new THREE.WebGLRenderer({{ antialias: true }});
            renderer.setSize(window.innerWidth, window.innerHeight);
            document.body.appendChild(renderer.domElement);
            
            // Lighting
            const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
            scene.add(ambientLight);
            
            const pointLight1 = new THREE.PointLight(0xffffff, 1);
            pointLight1.position.set(10, 10, 10);
            scene.add(pointLight1);
            
            const pointLight2 = new THREE.PointLight(0xffffff, 0.5);
            pointLight2.position.set(-10, -10, -10);
            scene.add(pointLight2);
            
            // Create material
            const material = new THREE.MeshStandardMaterial({{
                color: {props['color']},
                metalness: {props['metalness']},
                roughness: {props['roughness']},
                transparent: {'true' if material_type == 'Glass' else 'false'},
                opacity: {'0.6' if material_type == 'Glass' else '1.0'}
            }});
            
            // Create geometry based on shape
            let geometry;
            let mesh;
            
            const shapeType = "{props['shape']}";
            
            if (shapeType === "bottle") {{
                // Bottle shape using cylinders
                const group = new THREE.Group();
                
                // Body
                const bodyGeom = new THREE.CylinderGeometry(0.8, 0.8, 3, 32);
                const body = new THREE.Mesh(bodyGeom, material);
                group.add(body);
                
                // Neck
                const neckGeom = new THREE.CylinderGeometry(0.3, 0.3, 1, 32);
                const neck = new THREE.Mesh(neckGeom, material);
                neck.position.y = 2;
                group.add(neck);
                
                // Cap
                const capGeom = new THREE.CylinderGeometry(0.35, 0.35, 0.3, 32);
                const cap = new THREE.Mesh(capGeom, material);
                cap.position.y = 2.65;
                group.add(cap);
                
                mesh = group;
            }} else if (shapeType === "can") {{
                // Can shape
                geometry = new THREE.CylinderGeometry(0.6, 0.6, 2.5, 32);
                mesh = new THREE.Mesh(geometry, material);
            }} else if (shapeType === "box") {{
                // Box shape
                geometry = new THREE.BoxGeometry(2, 2, 2);
                mesh = new THREE.Mesh(geometry, material);
            }} else {{
                // Default sphere
                geometry = new THREE.SphereGeometry(1.5, 32, 32);
                mesh = new THREE.Mesh(geometry, material);
            }}
            
            scene.add(mesh);
            camera.position.z = 6;
            
            // Mouse controls
            let isDragging = false;
            let previousMousePosition = {{ x: 0, y: 0 }};
            
            renderer.domElement.addEventListener('mousedown', (e) => {{
                isDragging = true;
            }});
            
            renderer.domElement.addEventListener('mousemove', (e) => {{
                if (isDragging) {{
                    const deltaMove = {{
                        x: e.offsetX - previousMousePosition.x,
                        y: e.offsetY - previousMousePosition.y
                    }};
                    
                    mesh.rotation.y += deltaMove.x * 0.01;
                    mesh.rotation.x += deltaMove.y * 0.01;
                }}
                
                previousMousePosition = {{
                    x: e.offsetX,
                    y: e.offsetY
                }};
            }});
            
            renderer.domElement.addEventListener('mouseup', (e) => {{
                isDragging = false;
            }});
            
            // Zoom with mouse wheel
            renderer.domElement.addEventListener('wheel', (e) => {{
                e.preventDefault();
                camera.position.z += e.deltaY * 0.01;
                camera.position.z = Math.max(3, Math.min(15, camera.position.z));
            }});
            
            // Animation
            function animate() {{
                requestAnimationFrame(animate);
                
                // Auto-rotate when not dragging
                if (!isDragging) {{
                    mesh.rotation.y += 0.005;
                }}
                
                renderer.render(scene, camera);
            }}
            animate();
            
            // Handle window resize
            window.addEventListener('resize', () => {{
                camera.aspect = window.innerWidth / window.innerHeight;
                camera.updateProjectionMatrix();
                renderer.setSize(window.innerWidth, window.innerHeight);
            }});
        </script>
    </body>
    </html>
    """
    
    # Display the 3D model
    components.html(html_code, height=600)
    
    # Add download info
    st.info(f"✨ 3D Model generated for: **{material_type}** - {custom_prompt if custom_prompt else 'Generic item'}")
    st.markdown("**Features:**")
    st.markdown("- 🖱️ Click and drag to rotate")
    st.markdown("- 🔍 Scroll to zoom in/out")
    st.markdown("- 🎨 Material properties applied based on waste type")
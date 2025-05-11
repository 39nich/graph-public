# Accessible Graph Reader – README

This project is a full-stack web application designed to improve the accessibility of graphs for users who are blind or visually impaired. It enables users to upload a graph image and receive a multimodal representation of the graph—combining haptic, audio, and textual feedback to support non-visual graph comprehension.

## Features

- Graph Upload Interface – Users can upload PNG or JPEG graph images via the homepage.
- AI-Powered Graph Interpretation – Uses OpenAI’s GPT-4 Vision API to extract graph metadata and coordinate data from images.
- Accessible Graph Rendering – A canvas-based interface enables users to explore the graph by tracing the graph line with finger or mouse input.
- Multimodal Feedback – Provides haptic vibration and audio cues when the user interacts with the graph line.
- Screen Reader Support – HTML and Vue components are structured semantically with ARIA labels and WCAG 2.2 compliance in mind.
- Simple Navigation – Designed as a single-page application with three main views: Home, Help, and Graph Viewer.

## Technologies Used

- Frontend: Vue 3 (Composition API), HTML, CSS, JavaScript/TypeScript
- Backend: Django (Python)
- AI Integration: OpenAI GPT-4 Vision API
- HTTP Client: Axios (for frontend-backend communication)
- Accessibility: WCAG 2.2 guidelines, ARIA labelling, responsive design

## File Structure Overview
/frontend
├── views/
├── components/
├── utils/
├── router/
└── App.vue

/backend
├── convert/
│ └── gpt_vision.py
├── configuration/
│ └── urls.py
└── .env

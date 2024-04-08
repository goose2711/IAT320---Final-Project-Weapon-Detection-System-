# IAT320---Final-Project-Weapon-Detection-System-
Final Project for IAT320 - Stealth Shield (A Weapons Detection Software)
#(Programmer: Agastya Oruganti)
#(Designer: Zhaniya Yeltindinova)
#(Project Manager: Jihoon Lee)

Overview
This application harnesses the power of the YOLOv5 model, fine-tuned on the COCO128 dataset, to detect weapons in real-time video feeds. The development process encompassed the following steps:

Model Preparation: We initiated our project by cloning the YOLOv5 repository and selecting the COCO128.yaml dataset as our training base. This choice provided a diverse and robust starting point for object detection tasks.

Model Training and Fine-Tuning: After setting up the model environment, we proceeded with training, placing a strong emphasis on hyperparameter optimization to enhance detection performance. This meticulous tuning process ensured our model's accuracy and efficiency in real-world scenarios.

Model Exportation: Upon achieving satisfactory training results, we exported the model weights. This crucial step made it possible to integrate our trained model into various applications, ensuring versatility and ease of use.

Application Interface Development: Using Tkinter, we crafted a user-friendly interface that allows seamless interaction with the application. This interface includes essential functionalities such as model loading and real-time video feed display.

Real-Time Detection and Alert System: We implemented an advanced detection mechanism that utilizes the camera's video feed, processed through OpenCV, to identify weapons in real-time. The application draws bounding boxes around detected weapons, enhances user awareness through a blinking screen effect, and triggers an alarm sound to alert the user—all executed concurrently with the help of threading.

Documentation and Storage: The application is designed to record and store footage of detected weapons locally, providing a valuable resource for review and evidence.

This weapon detection application represents a significant step forward in ensuring safety and security through the use of advanced object detection technology.

import cv2

# Haar Cascade sınıflandırıcısını yüz tanıma için yükle
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Kamera numarasını belirtin (varsayılan olarak genellikle 0)
camera_number = 0

# Kamera bağlantısını açın
cap = cv2.VideoCapture(camera_number)

while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        break

    # Görüntüyü yatay olarak çevir (ayna etkisi)
    frame = cv2.flip(frame, 1)
    # Görüntüyü gri tonlamalıya çevir
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Yüzleri tespit et
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    # Kare boyutunu ve merkez koordinatlarını belirleme
    square_size = 300  # Kare kenar uzunluğu
    frame_height, frame_width, _ = frame.shape
    center_x = frame_width // 2
    center_y = frame_height // 2
    # Kare çizimi için köşe koordinatları ve renk belirleme
    start_point = (center_x - square_size // 2, center_y - square_size // 2)
    end_point = (center_x + square_size // 2, center_y + square_size // 2)
    color = (255, 0, 0)  # Mavi renk (BGR formatında)
    thickness = 3 # Kare kenarının kalınlığı

    # Kareyi çizme
    frame_with_square = cv2.rectangle(frame, start_point, end_point, color, thickness)
    for (x, y, w, h) in faces:
        # Yüzü çerçeve içine al
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

        # Yüzün merkez koordinatlarını hesapla
        face_center_x = x + w // 2
        face_center_y = y + h // 2

        # Kameranın merkezini hesapla
        frame_height, frame_width, _ = frame.shape
        camera_center_x = frame_width // 2
        camera_center_y = frame_height // 2
        print(frame_width," ",frame_height)
        # Pembe renginde ve 4 kalınlığında doğru çizme (yüz merkezinden kamera merkezine doğru)
        cv2.line(frame, (face_center_x, face_center_y), (camera_center_x, camera_center_y), (255, 255, 255), 4)

    text = f'YOUR FACE ({face_center_x}, {face_center_y})'
    cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    # Kareli görüntüyü göster
    cv2.imshow("Camera Feed with Face Detection", frame)
    # print("x konumu: y konumu: ",face_center_x,face_center_y)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

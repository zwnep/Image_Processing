# Image_Processing
Pyqt5 kullanarak bir görüntü işleme uygulaması tasarlama 

PyQt5 tarafından uygulanan görüntü işleme kullanıcı arayüzü. Program ile eşik, evrişim, morfolojik algoritmalar dahil olmak üzere bazı geleneksel görüntü işleme algoritmalarını uygular.


Ana Pencere:

Ana pencerede çeşitli alt pencerelere erişim sağlayan butonlar bulunmaktadır. 
Kullanıcı, ilgili butona tıklayarak istenilen alt pencereye erişebilir.  

![image](https://github.com/zwnep/Image_Processing/assets/71128703/675824b8-4a8f-4c7f-89b9-bded93a5a70f)



ChildWindow1: Histogram ve Eşikleme  Histogram Analizi 
- Görüntünün histogramını gösterir.
- Eşikleme: Manuel eşik belirleme, Otsu ve Entropy yöntemleriyle otomatik eşikleme.

![image](https://github.com/zwnep/Image_Processing/assets/71128703/e5d71111-5e8c-4813-926d-727035995975)



ChildWindow2: Konvolüsyon ve Filtreler  
- Konvolüsyon Operasyonu: Görüntü üzerinde konvolüsyon işlemi uygular.
- Filtreler: Robert, Prewitt, Sobel operatörleri ile kenar tespiti; Gaussian ve Median filtreler ile gürültü azaltma.

![image](https://github.com/zwnep/Image_Processing/assets/71128703/e0f2f111-3e1b-47c8-b038-518e19412aa4)



ChildWindow3: Temel İkili Morfolojik Algoritmalar  
İşlemler: İkili görüntülerde genişleme, erozyon, açma ve kapama işlemleri. 

![image](https://github.com/zwnep/Image_Processing/assets/71128703/81f991b1-f871-4039-8b99-216c44788907)



ChildWindow4: Gelişmiş İkili Morfolojik Algoritmalar  
İşlemler: Morfolojik mesafe dönüşümü, iskelet ve iskelet restorasyonu. 

![image](https://github.com/zwnep/Image_Processing/assets/71128703/6b2d7b70-38f6-436c-94a9-cf26c1f20e12)



ChildWindow5: Temel Gri Tonlamalı Morfolojik Algoritmalar  
İşlemler: Gri tonlamalı görüntülerde genişleme, erozyon, açma ve kapama işlemleri. 

![image](https://github.com/zwnep/Image_Processing/assets/71128703/72e2122c-2d8b-4a71-a140-8688427ccd07)



ChildWindow6: Gelişmiş Gri Tonlamalı Morfolojik Algoritmalar  
İşlemler: Morfolojik kenar tespiti, morfolojik rekonstrüksiyon, koşullu genişleme ve gri tonlama rekonstrüksiyonu. 

![image](https://github.com/zwnep/Image_Processing/assets/71128703/0a54ae57-dbd7-4473-8df2-9121e0e69a9b)





PyQt5 ile tasarlanan arayüz, kullanıcıların görüntü işleme algoritmalarını görsel olarak anlamalarını ve uygulamalarını kolaylaştırır. 

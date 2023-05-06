# SW 등록신고서

---

## 명칭

- 국문 : `객체 탐지를 활용한 인구밀집에 따른 경고 알림 시스템`

- 영문 : `A Warning notification system for population concentration using object detection`

- 적용 분야 : 공공 안전 관리, 시설 안전 관리, 교통 관리

---

## 주요기능

- 특정 구간의 카메라 모듈이 데이터를 수집하고 시스템 제어부를 통해 데이터를 서버로 송신한다.

- 서버는 카메라 모듈의 시스템 제어부와 통신하여 데이터를 수신하고 객체 탐지 모델을 사용한 딥러닝으로 특정 구간에 있는 사람들의 수를 계산하여 병목 현상을 탐지한다.

---

## 사용방법

- **(다음 모든 명령어는 Terminal 에서 실행한다.)**

- **(클라이언트 프로그램과 서버 프로그램은 같은 IP에서 동작해야한다.)**

- **_클라이언트 (Linux) 설정_**

1. 기본 요구사항

   - MCU : 라즈베리파이3B+ 이상

   - Python 3.8 버전 이상

2. 라즈베리파이에 삽입할 SD카드에 Raspiberry Pi Imager를 이용하여 라즈비안을 설치한다.

3. 라즈비안 설치 이후, SD카드에 ‘wpa_supplicant.conf’ 파일을 생성하여 서버와 통신할 무선 네트워크를 설정한다.

```
country=US
ctr1_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
network={
    ssid=“네트워크이름”
    psk=“네트워크비밀번호”
    scan_ssid=1
    key_mgmt=WPA-PSK
}
```

4. wpa_supplicant.conf 설정 이후, SD카드를 라즈베리파이에 장착하여 라즈베리파이에 전원을 공급한다.

5. 라즈베리파이를 원격으로 제어하기 위해 Putty를 이용하여 라즈베리파이에 원격으로 접속한다. (Putty가 설치되어 있는 PC와 라즈베리파이에 등록했던 Wifi가 같은 환경에 있어야 한다.)

6. 라즈베리파이에 원격으로 접속한 후, WebCam 기능을 활성화 시키기 위해 터미널을 통해 아래 라이브러리를 설치한다.

```
sudo apt-get update
sudo apt-get install motion
```

7. 설치 이후 motion.conf 파일에 진입하여 기본 설정을 변경한다.

```
sudo nano /etc/motion/motion.conf

# 변경사항
daemon off -> on
webcontrol_localhost on -> off
stream_localhost on -> off
output_pictures on -> off
ffmpeg_output_movies on -> off
```

8. 기본설정을 마친 후, 라즈베리파이에서 Client 파일을 실행하도록 ObjectDetection_Clnt.py 를 라즈베리파이에 코드를 옮긴다.

9. 서버 코드가 실행된 후 터미널을 통해 Client 코드를 실행한다.

```
python ObjectDetection_Clnt.py
```

- **_서버 (macOS(M1)) 설정_**

1. ObjectDetection.zip 을 압축해제한 후 ObjectDetection_Srv.py 스크립트와 haarcascades 폴더를 원하는 경로에 저장한다.

2. Homebrew 를 사용하여 OpenCV 및 NumPy를 설치하기 위해 다음과 같은 명령어를 입력한다.

```
brew install opencv
brew install numpy
```

3. Homebrew 를 사용하여 Python3 을 설치하기 위해 다음과 같은 명령어를 입력한다.

```
brew install python
```

4. 가상 환경 생성 및 활성화를 위해 다음과 같은 명령어를 입력한다.

```
python -m venv env
source env/bin/activate
```

5. 필요한 패키지를 모두 설치하기 위해 다음과 같은 명령어를 입력한다.

```
pip install opencv-python-headless
```

6. Python 스크립트를 실행하기 위해 다음과 같은 명령어를 입력한다. 이 때, path 는 1 에서 ObjectDetection_Srv.py 스크립트와 haarcascades 폴더를 저장한 실제 경로이다.

```
cd path
python ObjectDetection_Srv.py
```

- **_프로그램 실행_**

1. ObjectDetection_Clnt.py 서버 IP 와 port 로 바꾼 후 실행한다.

```
server_address = ('server_ip', server_port)
```

2. 서버에서 ObjectDetection_Srv.py 를 실행한 후 클라이언트에서 ObjectDetection_Clnt.py 를 실행한다.

---

## 프로그램 설정

- 사용 OS

  - 클라이언트 : Linux

  - 서버 : macOS (M1)

- 사용 언어

  - Python 3.9

- 필요한 프로그램

  - OpenCV 4.7.0

  - NumPy 1.23.5

---

from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import redirect
from .models import User
import pyaudio,wave
import pyaudio
import wave
import keyboard
import numpy as np



# Create your views here.
def home_view(request):
    return render(request, "users/home.html")
def login_view(request):
    if request.method == "POST":
        #print(request.POST)
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username = username, password =password)
        if user is not None:
            print("인증성공")
            login(request, user)
        else:
            print("인증실패")
    return render(request, "users/login.html")

def logout_view(request):
    logout(request)
    return redirect("user:login")

def signup_view(request):
    if request.method =="POST":
        print(request.POST)
        print(222,request.FILES)
        profile_img = request.FILES["profile_img"]
        username = request.POST["username"]
        password = request.POST["password"]
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        email = request.POST["email"]
        student_id = request.POST["student_id"]


        user = User.objects.create_user(username, email, password)
        user.last_name = lastname
        user.first_name = firstname
        user.student_id = student_id
        user.profile_img = profile_img
        user.save()

        return redirect("user:login")

    return render(request, "users/signup.html")

def recording_view(request):
    CNT = np.random.randint(0,9999)
    
    if "btn_record" in request.GET:
        
        print("start record")
        audio = pyaudio.PyAudio()
        stream =audio.open(format=pyaudio.paInt16,channels=1,rate =44100,input=True,frames_per_buffer=1024)

        frames =[]
        
        
        while True:
            
            data = stream.read(1024)
            frames.append(data)
        
            if keyboard.is_pressed("ESC"):
                
                print("stop and saving")
                break
            
        stream.stop_stream()
        stream.close()
        audio.terminate()

        sound_file = wave.open(f"voice/myrecording{str(CNT)}.wav","wb")
        sound_file.setnchannels(1)
        sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        sound_file.setframerate(44100)
        sound_file.writeframes(b''.join(frames))
        sound_file.close()
        CNT += 1
        

    return render(request, "users/recording.html")
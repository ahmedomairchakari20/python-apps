from django.contrib.auth import authenticate
from .models import User, Task, Profile
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.files.base import ContentFile
from rest_framework.views import APIView
from rest_framework.response import Response
import matplotlib.pyplot as plt
from datetime import date, timedelta, datetime, time
from django.db.models import Count
from django.db.models import Q
from django.db.models.functions import ExtractMonth
import datetime as dt
from .helper import send_forget_password_email
import uuid
import json
from bs4 import BeautifulSoup
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from .helper import send_

class DefaultView(APIView):
    def get(self, request):
        print(request.data)

        user = User.objects.filter(email='radcowboy@example.com')
        print(user)
        for u in user:
            print(type(u))
            print(type(u.is_active))
        return Response(f"heloww")

    def post(self, request):
        print(request.data)
        # serializer = UserRegistrationSerializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # user = serializer.save()
        # token = get_tokens_for_user(user)
        return Response({'token':'omw', 'msg':'Registration Successful'})


def auth(email, password):
    user = User.objects.get(email = email)
    if user:
        print("user exists")
        if user.check_password(password):
            return user
    return None

class UserLoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        print(email, password)

        user = auth(email=email, password=password)
        if user is not None:
            print(user)
            #  token = get_tokens_for_user(user)
            return Response({"email": user.email})
        else:
            return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}})

          
class SignupView(APIView):
    def get(self, request):
          print(request.data)
          return Response({"msg": "success"})
    
    def post(self, request):

        print(request.data)
        email = request.data['email']
        uname = request.data['username']
        password = request.data['password']
        print(email, uname, password)

        try:
            new_user = User.objects.create_user(
                email=email, password=password, username=uname
            )
            new_user.save()
        except:
            user = User.objects.get(email=email)
            
            print(user.email)
            print(type(user.email))
            user_info = {"email": user.email, "name": user.name}
            return Response(user_info)
        # print(new_user.email)
        return Response({"msg": "success bby"})
        # return Response({"email": new_user.email, "name": new_user.name})
        

class ProfileData(APIView):
    def get(self, request):
        # Retrieve the authenticated user
        email = request.GET.get("email")
        print(email)
        user = User.objects.get(email=email)
        print(user.notify)

        # Retrieve the user's profile data
        profile = Profile.objects.get(user=user)

        if profile:
            #Prepare the profile data to be returned
            profile_data = {
                "name": profile.name,
                "occupation": profile.occupation,
                "age": profile.age,
                "email": user.email,
                "notify":user.notify,
                "media": profile.media.url if profile.media else None,
            }

        return Response(profile_data)
    def post(self,request):
        print("media",request.data.get('media'))
        # Retrieve user information from the request (assuming the user is authenticated)
        email = request.data.get('email')
        user = User.objects.get(email=email)
       
        # Retrieve the data from the request
        name = request.data.get('name')
        occupation = request.data.get('occupation')
        age = request.data.get('age')
        notify=request.data.get('notify')
        media = request.data.get('media')  # Assuming media is sent as a file in the request
        # Check if a profile already exists for the user
        if notify=="false":
            notif=False
        else:
            notif=True
        print(notif)
        user.notify=notif
        user.save()
        profile, created = Profile.objects.get_or_create(user=user)
        

        # Update the profile data
        profile.name = name
        profile.occupation = occupation
        profile.age = age
        if media:
            profile.media = media

        # Save the profile object
        profile.save()

        return Response({'msg': "Profile data saved successfully."})
        


class ForgetPasswordView(APIView):
    def post(self, request):
        email = request.data['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"msg": "User Not Found"})
        print(user.id)
        
        return Response({"msg": "user exist"})

class changepassword(APIView):
    def post(self, request):
        token = request.data['token']
        print(token)
        user=User.objects.get(email=token)

        return Response({"user_id": user.id})
        

class newPassword(APIView):
    def post(self,request):
        user_id=request.data['user_id']
        password=request.data['password']
        print(user_id,password)
        try:
            user = User.objects.get(id=user_id)
            user.set_password(password)
            user.save()
            return Response({"msg":"password changed successfully"})
        except Exception as e:
            print(e)
            return Response({"msg":"user_id doesnt exist"})
        

def dateFormat(date_str):
    date_obj = datetime.strptime(str(date_str), "%Y-%m-%d")

    day = date_obj.day
    month = date_obj.strftime("%b")
    year = date_obj.year
    formatted_date = f"{day} {month} {year}"
    # print(formatted_date)  # Output: "12 April"
    return formatted_date

def timeFormat(time_str):
    time_obj = datetime.strptime(str(time_str), "%H:%M:%S")

    formatted_time = time_obj.strftime("%I:%M %p")
    # print(formatted_time)  # Output: "11:00 AM"
    return formatted_time


def getForwardProgressTime(future_date):
    future_date = future_date.strftime('%Y-%m-%d %H:%M:%S')
    dt = datetime.strptime(future_date, '%Y-%m-%d %H:%M:%S')

    time_difference = datetime.now() - dt 
    minutes_difference = int(time_difference.total_seconds() / 60)
    hours_difference = int(time_difference.total_seconds() / 3600)
    days_difference = time_difference.days
    print(minutes_difference)
    print(hours_difference)
    print(days_difference)
    if abs(days_difference) >= 1:
        return f"{abs(days_difference)} Days"
    elif abs(hours_difference) >=1: 
        return  f"{abs(hours_difference)} Hours"
    else:
        return f"{abs(minutes_difference)} Minutes"

def getProgressTime(previous_date): # on complete calculate total time
    # print(previous_date)

    time_difference = datetime.now() - previous_date
    minutes_difference = int(time_difference.total_seconds() / 60)
    hours_difference = int(time_difference.total_seconds() / 3600)
    days_difference = time_difference.days
    
    if abs(days_difference) >= 1:
        return f"{abs(days_difference)} Days"
    elif abs(hours_difference) >=1: 
        return  f"{abs(hours_difference)} Hours"
    else:
        return f"{abs(minutes_difference)} Minutes"
    
def trimDescription(html_string):
    # Parse the HTML string
    soup = BeautifulSoup(html_string, "html.parser")

    # Get the text content from the HTML
    text_content = soup.get_text()

    # Truncate the text content to a maximum of 50 characters
    truncated_text = f'<br/><p>{text_content[:50]}</p><br/>'
    print(truncated_text)

    return truncated_text
class TaskView(APIView):
     
     def get(self, request, ):
        print(request.GET.get("email"))
        email = request.GET.get("email")
        user = User.objects.get(email=email)

        current_time = datetime.now()
        current_date = date.today()

        time_obj = current_time.time()

        print(time_obj)

        # future tasks
        upcoming_tasks = Task.objects.filter(created_by=user,is_complete=False, is_started=False).filter(date__gt=current_date)
        upcoming_tasks2 = Task.objects.filter(created_by=user,is_complete=False, is_started=False).filter(date=current_date).filter(time__gt=time_obj)
        upcoming_tasks = (upcoming_tasks | upcoming_tasks2 ).order_by('date')

        print(upcoming_tasks)
        previous_tasks = Task.objects.filter(created_by=user,is_complete=False, is_started=False).filter(date__lt=current_date)
        previous_tasks2 = Task.objects.filter(created_by=user,is_complete=False, is_started=False).filter(date=current_date).filter(time__lt=time_obj)
        previous_tasks = (previous_tasks | previous_tasks2 ).order_by('date')
        # upcoming_tasks = upcoming_tasks | previous_tasks
        print(upcoming_tasks)
        inprogress_tasks = Task.objects.filter(created_by=user,is_complete=False, is_started=True).order_by('date')

        completed_tasks = Task.objects.filter(created_by=user, is_complete= True).order_by('date')

        U_tasks = []
        P_tasks = []
        D_tasks = []
        for uc_task in upcoming_tasks:
            # get all t
            pdate = dateFormat(uc_task.date)
            ptime = timeFormat(uc_task.time)
            # print(uc_task.image.url)
            task ={
                'id': uc_task.id,
                'title': uc_task.title,
                'description': uc_task.description,
                "date": pdate,
                "time": ptime,
                'color': uc_task.color,
                "complete_percentage": uc_task.complete_percentage,
                "recurring_task": uc_task.recurring_task,
                "recurring_task_date": uc_task.recurring_task_date,
                # "image": uc_task.image.url or ''
                "image": uc_task.image.url if uc_task.image else None,

            }
            U_tasks.append(task)
            
        for uc_task in previous_tasks: # expired tasks
            pdate = dateFormat(uc_task.date)
            ptime = timeFormat(uc_task.time)
            task ={
                'id': uc_task.id,
                'title': uc_task.title,
                'description': uc_task.description,
                "date": pdate,
                "time": ptime,
                'color': uc_task.color,
                "complete_percentage": uc_task.complete_percentage,
                "recurring_task": uc_task.recurring_task,
                "recurring_task_date": uc_task.recurring_task_date,
                "image": uc_task.image.url if uc_task.image else None,

            }
            U_tasks.append(task)
        print(U_tasks)
        for ip_task in inprogress_tasks:
            if ip_task.is_complete:
                continue
            pdate = dateFormat(ip_task.date)
            ptime = timeFormat(ip_task.time)
            task ={
                'id': ip_task.id,
                'title': ip_task.title,
                'description': ip_task.description,
                "date": pdate,
                "time": ptime,
                'complete_percentage': ip_task.complete_percentage,
                "color": ip_task.color,
                "recurring_task": ip_task.recurring_task,
                "recurring_task_date": ip_task.recurring_task_date,
                "image": ip_task.image.url if ip_task.image else None,

            }
            P_tasks.append(task)

        for d_task in completed_tasks:
            pdate = dateFormat(d_task.date)
            ptime = timeFormat(d_task.time)

            task ={
                'id': d_task.id,
                'title': d_task.title,
                'description': d_task.description,
                "date": pdate,
                "time": ptime,
                'color': d_task.color,
                'complete_percentage': d_task.complete_percentage,
                "recurring_task": d_task.recurring_task,
                "recurring_task_date": d_task.recurring_task_date,
                "image": d_task.image.url if d_task.image else None,
            }
            D_tasks.append(task)    
        
        data= {
            "upcoming":U_tasks,
            "inprogress":P_tasks,
            "complete":D_tasks
        }
        return Response(data)
     
     def post(self, request):
        print(request.data)
        email = request.POST.get('email')
        title = request.POST.get('title')
        description = request.POST.get('description').rstrip()
        date = request.POST.get('date')
        time = request.POST.get('time')
        # remindme = request.POST.get('remindMe')
        # remindme = remindme.lower() == 'true'
        # remindme_dates = json.loads(request.POST.get('remindMeDates'))
        # remindme_dates = [datetime.strptime(date, '%Y-%m-%d').date().isoformat() for date in remindme_dates]
        recurringtask = request.POST.get('recurringTask')
        recurringtask = recurringtask.lower() == 'true'
        recurringtask_dates = json.loads(request.POST.get('recurringTaskDates'))
        recurringtask_dates = [datetime.strptime(date, '%Y-%m-%d').date().isoformat() for date in recurringtask_dates]
        color = request.POST.get('color')
        existing_task = request.POST.get('existing')  
        existing_task = existing_task.lower() == 'true'
        day_limit = request.POST.get('dayLimit')
        day_limit = day_limit.lower() == 'true'
        image_file = request.FILES.get('media')
        print("image file:", image_file)
        print(recurringtask_dates)
        print("recurring",recurringtask)
        print("existing",existing_task)
        print("day",day_limit)
        user = User.objects.get(email=email)
          #first we wil check if the task is existed on the same date and time
        if existing_task == False:
              
            try:
                sameTask = Task.objects.filter(created_by=user, date=date, time=time)
                # print("same:", sameTask)
                if sameTask:
                    return Response({'exist': 'Same Task Exist on the same date and time, Are you sure to add this Task?'})
            except Exception as e:
                print("An error occurred:", str(e))

        if day_limit== False:
              
            try:
                all_day_task = Task.objects.filter(created_by=user,date=date)
                print(all_day_task)
                print(dt.date.today())
                print("count", all_day_task.count())
                if all_day_task.count() >= 5:
                    return Response({'limit': 'You have exceeded the limit of 5 tasks per day. Are You sure you want add more task?'})
            except Exception as e:
                print("An error occurred:", str(e))
              
            
        
          

        new_task = Task(
              title=title, recurring_task= recurringtask,
              description=description, date=date, time=time, color=color, created_by=user
              )
          
        new_task.save()          
              
        if recurringtask == True:
              print("recurring task true")
              new_task.recurring_task_date = recurringtask_dates
              new_task.save()
        if image_file:
                new_task.image.save(image_file.name, ContentFile(image_file.read()), save=False)
                new_task.save()

        for d in recurringtask_dates:
                # recurring_d = datetime.strptime(d, "%Y-%m-%d").date()
                print(d)
                recur_task = Task(
                    title=title, recurring_task= False,
                    description=description, date= d, time=time, color=color, created_by=user,
                    parent_task = new_task.id
                )
                recur_task.save()
                if image_file:
                    recur_task.image.save(image_file.name, ContentFile(image_file.read()), save=False)
                    recur_task.save()


        #   print(new_task)
        #   print(new_task.created_by)
        send_(email,"New Task Added Title : "+title,"you have added a new task with description: '"+description+"'. And time details as follow\n Date: "+str(date)+"\n Time: "+str(time)+"\n")
        return Response({'msg':'Task Added Successfully'})
     
     def delete(self, request):
        email = request.GET.get("email")
        id = request.GET.get("id")
        print(email, id)
        user = User.objects.get(email=email)
        task = Task.objects.get(created_by=user, id=id)
        task.delete()
        return Response({"msg": "success"})
     
     def patch(self, request):
        # get all the attribute
        id=request.POST.get('id')
        email = request.POST.get('email')
        title = request.POST.get('title')
        description = request.POST.get('description').rstrip()
        date = request.POST.get('date')
        time = request.POST.get('time')
        # remindme = request.POST.get('remindMe')
        # remindme = remindme.lower() == 'true'
        # remindme_dates = json.loads(request.POST.get('remindMeDates'))
        # remindme_dates = [datetime.strptime(date, '%Y-%m-%d').date().isoformat() for date in remindme_dates]
        recurringtask = request.POST.get('recurringTask')
        recurringtask = recurringtask.lower() == 'true'
        recurringtask_dates = json.loads(request.POST.get('recurringTaskDates'))
        recurringtask_dates = [datetime.strptime(date, '%Y-%m-%d').date().isoformat() for date in recurringtask_dates]
        color = request.POST.get('color')
        image_file = request.FILES.get('media')
        print("image file:", image_file)
        


        user = User.objects.get(email=email)
        task = Task.objects.get(created_by=user, id=id)
        task.title = title
        task.description = description
        task.date = date
        task.time = time
        task.recurring_task = recurringtask
        task.recurring_task_date = recurringtask_dates
        if image_file is not None:
            print("image file:", image_file)
            task.image= image_file
        # do something with those new dates like create a task on those dates & delete prevs
        # all those with same title description color time
        
        # create them tasks
        children_tasks = Task.objects.filter(parent_task = task.id) # [8, 10]
        child_task_dates = []
        for ct in children_tasks:
            child_task_dates.append(str(ct.date))


        for child_task_date in task.recurring_task_date:
            if child_task_date not in child_task_dates: # a new task, [8, 11, 15]
                new_task =  Task(
                    title=title, recurring_task= False,
                    description=description, date= child_task_date, time=time, color=color, created_by=user,
                    parent_task = task.id
                )
                new_task.save()
                if image_file:
                    new_task.image.save(image_file.name, ContentFile(image_file.read()), save=False)
                    new_task.save()
                
        # I have 2 children of drip hard task
        # I remove 1 from there and added
        #     
        # get all child aka tasks where parent = task.id
        # check if task.date in task.recurring_task_date[]
        # if not then delete that child
        children_tasks = Task.objects.filter(parent_task = task.id)

        for child_task in children_tasks:
            if str(child_task.date) not in task.recurring_task_date:
                child_task.delete()

        task.color = color
        

        task.save()

        return Response({"msg": "updated"})

class TaskPercentage(APIView):
    def patch(self, request):
        email = request.data["email"]
        id = request.data["id"]
        percentage = request.data['percentage']
        print(email, id, percentage)
        user = User.objects.get(email=email)
        task = Task.objects.get(created_by=user, id=id)
        task_dt = datetime.combine(task.date, task.time)
        current_time = datetime.now()
        

        if percentage == 100:
            task.is_complete = True
            print(task.date)
            print(task.time)
            dt = datetime.combine(task.date, task.time)
            if task_dt > current_time:
                print(dt)
                if task.start_datetime == None:
                    task.complete_date = '0 Days'
                    task.complete_percentage = percentage
                    task.save()
                    return Response({"msg": "updated"})
                else:    
                    task.complete_date = getForwardProgressTime(task.start_datetime)
            else:    
                task.complete_date = getProgressTime(dt) # 380 days
            print("Task updated")

        task.complete_percentage = percentage
        task.save()

        if task_dt > current_time: # future
            if task.start_datetime == None:
                task.start_datetime = current_time                
            print('this executes for future tasks')
            print(current_time)

        return Response({"msg": "updated"})

class ProgressView(APIView): # all i have to do is shift
    def patch(self, request):
        email = request.data["email"]
        id = request.data["id"]

        user = User.objects.get(email=email)
        task = Task.objects.get(created_by=user, id=id)
        task.is_started = True # query the inprogress tasks if there is_started is true
        task.start_datetime = datetime.now() # Task starts only when this is called
        task.save()

        send_(email,"Your Task '"+task.title+"' has been moved to In progress",
              "Your Task has description: '"+task.description+"' . And time details as follow\n Date: "+str(task.date)+"\n Time: "+str(task.time)+"\n")
        return Response({"msg": "updated"})

class CompleteView(APIView): # all i have to do is shift
    def patch(self, request):
        email = request.data["email"]
        id = request.data["id"]
        print("in complete req")
        user = User.objects.get(email=email)
        task = Task.objects.get(created_by=user, id=id)
        task.is_complete = True # query the inprogress tasks if there is_started is true
        task.complete_percentage = 100
        
        task_dt = datetime.combine(task.date, task.time)
        current_time = datetime.now()

        if task_dt > current_time:
            if task.start_datetime == None:
                task.complete_date = '0 Days'
                task.save()
                return Response({"msg": "updated"})
            else:    
                task.complete_date = getForwardProgressTime(task.start_datetime)
        else:    
            task.complete_date = getProgressTime(task_dt) # 380 days
        
        
        task.save()
        send_(email,"Congratulations on Completing Your Task '"+task.title+"'.","Your Task has description: '"+task.description+"' .")

        return Response({"msg": "updated"})
    
    def delete(self, request):

        email = request.GET.get("email")
        # print(email, id)
        user = User.objects.get(email=email)
        # all the completed tasks of the current user
        
        tasks = Task.objects.filter(created_by=user).filter(created_by=user, is_complete= True).order_by('date')
        print(tasks)
        tasks.delete()
        return Response({"response": "Deleted"})

class UpdateProfileView(APIView):

    def post(self, request):
        print(request.data)
        email = request.data["email"]
        age = request.data["age"]
        occupation = request.data["occupation"]
        name = request.data["name"]

        user = User.objects.get(email=email)
        user.age = age
        user.occupation = occupation
        user.name = name

        user.save()
        return Response({"msg": "success"})  
    

class DashboardView(APIView):
    def get(self, request):
        email = request.GET.get("email")
        user = User.objects.get(email=email)
        # Tasks that have is_completed = True are complete
        # Tasks that have completed_percentage = zero are upcoming
        # Tasks that have completed_percentage > 0 are in-progress & whose date is past current
        # query for upcoming
        upcoming_tasks = Task.objects.filter(created_by=user, is_complete=False, is_started=False).order_by('date')
        
        # filter(created_by=user, date__gte=date.today(), time__gte= time_obj, complete_percentage=0).order_by('date') # 30 april, 2023 1pm
        inprogress_tasks = Task.objects.filter(created_by=user,is_complete=False, is_started=True).order_by('date')

        # query for completed
        completed_tasks = Task.objects.filter(created_by=user, is_complete= True)
        tasks = Task.objects.filter(created_by=user)

        data = {
            "upcoming_tasks": len(upcoming_tasks),
            "inprogress_tasks": len(inprogress_tasks),
            "completed_tasks": len(completed_tasks),
            "total": len(tasks)
        }
        print(tasks)
        
        return Response(data)    

class SearchView(APIView):
    def get(self, request):
        email = request.GET.get("email")
        user = User.objects.get(email=email)
        search = request.GET.get("search")
        print(f"search value is: {search}")
        current_time = datetime.now()
        time_obj = current_time.time()
        data = {
                "upcoming":[],
                "inprogress":[],
                "complete":[]
            }
        if search:
            tasks = Task.objects.filter(title__icontains=search, created_by=user)
            # do the same stuff you do for that
            upcoming_tasks = tasks.filter(is_complete=False, is_started=False)

            inprogress_tasks = tasks.filter(created_by=user, is_complete=False, is_started=True).order_by('date')

            completed_tasks = tasks.filter(created_by=user, is_complete= True).order_by('date')

            U_tasks = []
            P_tasks = []
            D_tasks = []
            for uc_task in upcoming_tasks:
                pdate = dateFormat(uc_task.date)
                ptime = timeFormat(uc_task.time)
                task ={
                    'id': uc_task.id,
                    'title': uc_task.title,
                    'description': uc_task.description,
                    "date": pdate,
                    "time": ptime,
                    "complete_percentage": uc_task.complete_percentage,
                    "color": uc_task.color,
                    "image": uc_task.image.url if uc_task.image else None,

                }
                U_tasks.append(task)

            for ip_task in inprogress_tasks:
                if ip_task.is_complete:
                    continue
                pdate = dateFormat(ip_task.date)
                ptime = timeFormat(ip_task.time)
                task ={
                    'id': ip_task.id,
                    'title': ip_task.title,
                    'description': ip_task.description,
                    "date": pdate,
                    "time": ptime,
                    'complete_percentage': ip_task.complete_percentage,
                    "color": ip_task.color,
                    "image": ip_task.image.url if ip_task.image else None,

                }
                P_tasks.append(task)

            for d_task in completed_tasks:
                pdate = dateFormat(d_task.date)
                ptime = timeFormat(d_task.time)

                task ={
                    'id': d_task.id,
                    'title': d_task.title,
                    'description': d_task.description,
                    "date": pdate,
                    "time": ptime,
                    'complete_percentage': d_task.complete_percentage,
                    'color': d_task.color,
                    "image": d_task.image.url if d_task.image else None,
                    
                }
                D_tasks.append(task)    
            
            data= {
                "upcoming":U_tasks,
                "inprogress":P_tasks,
                "complete":D_tasks
            }

        return Response(data)
    
    def get(self, request):
        email = request.GET.get("email")
        user = User.objects.get(email=email)
        data = {
            "feedback": user.feedback,
        }
        return Response(data)
    def post(self,request):
        email=request.data['email']
        feedback=request.data['feedback']
        support=request.data['support']
        user = User.objects.get(email=email)
        user.feedback=feedback
        user.support=support
        user.save()
        # here email will be the admin email
        send_("rosebranch18@gmail.com","Support Needed","user email"+email+"\n"+"Support msg:"+support+"\n"+"Feedback:"+feedback+"\n")
        return Response({"msg": "feddback send to Admin"})
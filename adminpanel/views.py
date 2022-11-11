from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializers import *
from account.models import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from account.emails import *
from .serializers import *
from adminpanel.permissions import *
from datetime import date
from django.shortcuts import get_object_or_404


class AddStudent(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        allclasses = list(Class.objects.all())
        arr = []
        for clas in allclasses:
            arr += [[clas.year, clas.department.name, clas.section, clas.id]]
        arr.sort()
        return Response(arr, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = AddStudentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        name = serializer.data.get('name')
        DOB = serializer.data.get('DOB')
        classid = serializer.data.get('class_id')
        gender = request.data.get('sex')

        students = list(Student.objects.all())
        if len(students) != 0:
            userID = int(students[-1].userID)+1
        else:
            userID = 200000
        classid = get_object_or_404(Class, id=classid)
        # Default Password --> first_name in lowercase + @ + DOB(YYYYMMDD)
        password = name.split(" ")[0].lower() + '@' + DOB.replace("-", "")
        password = password[0].upper()+password[1:]

        try:
            user = User.objects.get(email=email)
            return Response({'msg': 'User with this email already exists'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            pass

        if gender is not None:
            if gender.lower() == 'm':
                sex = 'Male'
            elif gender.lower() == 'f':
                sex = 'Female'
            else:
                return Response({'msg': 'Invalid gender input'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            EMAIL.send_credentials_via_email(
                userID, password, name, email, 'student')
        except:
            return Response({'msg': 'Some error occured! Please try again'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            email=email,
            userID=userID,
            name=name,
        )
        user.set_password(password)
        user.is_stu = True
        user.save()
        Student(
            user=user,
            userID=userID,
            name=name,
            DOB=DOB,
            class_id=classid,
        ).save()
        curstu = Student.objects.get(userID=userID)
        if gender is not None:
            curstu.sex = sex
            curstu.save()
        return Response({'msg': 'Student Created Successfully'}, status=status.HTTP_200_OK)


class AddTeacher(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        alldepartments = list(Department.objects.all())
        dict = {}
        for dep in alldepartments:
            dict[dep.id] = dep.name
        return Response(dict, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = AddTeacherSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        name = serializer.data.get('name')
        DOB = serializer.data.get('DOB')
        department = serializer.data.get('department')
        gender = request.data.get('sex')

        teachers = Teacher.objects.all()
        try:
            userID = int(list(teachers)[-1].userID)+1
        except:
            userID = 100000

        department = get_object_or_404(Department, id=department)
        # Default Password --> first_name in lowercase + @ + DOB(YYYYMMDD)
        password = name.split(" ")[0].lower() + '@' + DOB.replace("-", "")
        password = password[0].upper()+password[1:]

        try:
            user = User.objects.get(email=email)
            return Response({'msg': 'User with this email already exists'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            pass

        if gender is not None:
            if gender.lower() == 'm':
                sex = 'Male'
            elif gender.lower() == 'f':
                sex = 'Female'
            else:
                return Response({'msg': 'Invalid gender input'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            EMAIL.send_credentials_via_email(
                userID, password, name, email, 'teacher')
        except:
            return Response({'msg': 'Some error occured! Please try again'}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(
            email=email,
            userID=userID,
            name=name,
        )
        user.set_password(password)
        user.is_tea = True
        user.save()

        Teacher(
            user=user,
            userID=userID,
            name=name,
            DOB=DOB,
            department=department
        ).save()
        curtea = Teacher.objects.get(userID=userID)
        if gender is not None:
            curtea.sex = sex
            curtea.save()
        return Response({'msg': 'Teacher Created Successfully'}, status=status.HTTP_200_OK)


class Departments(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request, pk):
        if pk == 'ALL':
            departments = Department.objects.all()
            serializer = DepartmentSerializer(departments, many=True)
        else:
            departments = get_object_or_404(Department, id=pk)
            serializer = DepartmentSerializer(departments, many=False)
        return Response(serializer.data)

    def post(self, request, pk):
        serializer = DepartmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Department added successfully'},  status=status.HTTP_200_OK)

    def put(self, request, pk):
        department = get_object_or_404(Department, id=pk)
        serializer = DepartmentSerializer(
            instance=department, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'msg': 'Department modified successfully'},  status=status.HTTP_200_OK)

    def delete(self, request, pk):
        department = get_object_or_404(Department, id=pk)
        department.delete()
        return Response({'msg': 'Department deleted successfully'},  status=status.HTTP_200_OK)


class ClassObject(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request, pk):
        if pk == 'ALL':
            allclasses = list(Class.objects.all())
            arr = []
            for clas in allclasses:
                arr += [[clas.year, clas.department.name, clas.section, clas.id]]
            arr.sort()
            return Response(arr, status=status.HTTP_200_OK)
        else:
            classes = get_object_or_404(Class, id=pk)
            serializer = ClassSerializer(classes, many=False)
            return Response(serializer.data)

    def post(self, request, pk):
        serializer = ClassSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'msg': 'Class added successfully'},  status=status.HTTP_200_OK)

    def put(self, request, pk):
        clas = get_object_or_404(Class, id=pk)
        serializer = ClassSerializer(instance=clas, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'msg': 'Class modified successfully'},  status=status.HTTP_200_OK)

    def delete(self, request, pk):
        clas = get_object_or_404(Class, id=pk)
        clas.delete()
        return Response({'msg': 'Class deleted successfully'},  status=status.HTTP_200_OK)


class ClassByDepartment(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request, departmentid):
        department = get_object_or_404(Department, id=departmentid)
        allclasses = Class.objects.all().filter(department=department)
        dict = {}
        for clas in allclasses:
            dict[clas.id] = {"year": clas.year, "section": clas.section}
        return Response(dict,  status=status.HTTP_200_OK)


class Subjects(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request, pk):
        if pk == 'ALL':
            subject = Subject.objects.all()
            serializer = SubjectSerializer(subject, many=True)
        else:
            subject = get_object_or_404(Subject, code=pk)
            serializer = SubjectSerializer(subject, many=False)
        return Response(serializer.data)

    def post(self, request, pk):
        serializer = SubjectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'msg': 'Subject added successfully'},  status=status.HTTP_200_OK)

    def put(self, request, pk):
        subject = get_object_or_404(Subject, code=pk)
        serializer = SubjectSerializer(instance=subject, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'msg': 'Subject modified successfully'},  status=status.HTTP_200_OK)

    def delete(self, request, pk):
        subject = get_object_or_404(Subject, code=pk)
        subject.delete()
        return Response({'msg': 'Subject deleted successfully'},  status=status.HTTP_200_OK)


class FeedbackView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request, key):
        resdict = {}
        if key.lower() == 'teachers':
            feedbacks = list(TeacherFeedback.objects.all())
            for feedback in feedbacks:
                try:
                    resdict[feedback.teacher.name] += [
                        {feedback.student.name: feedback.feed}]
                except:
                    resdict[feedback.teacher.name] = [
                        {feedback.student.name: feedback.feed}]
        elif key.lower() == 'students':
            feedbacks = list(StudentFeedback.objects.all())
            for feedback in feedbacks:
                try:
                    resdict[feedback.student.name] += [
                        {feedback.teacher.name: feedback.feed}]
                except:
                    resdict[feedback.student.name] = [
                        {feedback.teacher.name: feedback.feed}]
        else:
            user = get_object_or_404(User, userID=key)
            stu = user.is_stu
            tea = user.is_tea
            if stu:
                student = Student.objects.get(userID=key)
            elif tea:
                teacher = Teacher.objects.get(userID=key)
            else:
                return Response({'msg': 'INVALID INPUT'},  status=status.HTTP_400_BAD_REQUEST)
            c = 0
            tf = 0
            if stu:
                feedbacks = list(
                    StudentFeedback.objects.filter(student=student))
            else:
                feedbacks = list(
                    TeacherFeedback.objects.filter(teacher=teacher))
            for feedback in feedbacks:
                if stu:
                    resdict[feedback.teacher.name] = feedback.feed
                else:
                    resdict[feedback.student.name] = feedback.feed
                tf += feedback.feed
                c += 1
            avgfeed = tf/c
            resdict["averagefeed"] = avgfeed
        return Response(resdict,  status=status.HTTP_200_OK)


class CreateAttendance(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):
        serializer = CreateAttendanceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        start_date = serializer.data.get("start_date")
        end_date = serializer.data.get("end_date")
        class_id = serializer.data.get("class_id")
        sdate = date(int(start_date[:4]), int(
            start_date[5:7]), int(start_date[8:]))
        edate = date(int(end_date[:4]), int(end_date[5:7]), int(end_date[8:]))
        n = (edate - sdate).days
        cur = sdate
        curclass = get_object_or_404(Class, id=class_id)
        students = Student.objects.filter(class_id=curclass)
        days = {1: 'Monday', 2: 'Tuesday', 3: 'Wednesday',
                4: 'Thursday', 5: 'Friday', 6: 'Saturday', 0: 'Sunday'}
        for i in range(n+1):
            curdate = cur
            curday = days[int(cur.strftime('%w'))]
            cur += timedelta(days=1)
            if curday == 'Sunday':
                continue
            assignedtimes = AssignTime.objects.filter(
                day=curday, class_id=curclass)
            for assignedtime in assignedtimes:
                ca = ClassAttendance.objects.create(
                    date=curdate, assign=assignedtime)
                for student in students:
                    StudentAttendance.objects.create(
                        student=student, classattendance=ca, subject=assignedtime.assign.subject)

        return Response({'msg': 'Attendance Objects added successfully'},  status=status.HTTP_200_OK)

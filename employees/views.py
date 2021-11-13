import csv
import pandas as pd
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.parsers import MultiPartParser
from .models import Employee
from .serializers import EmployeeSerializer


class ListEmployeesAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, **kwargs):
        employees = Employee.objects.all()
        data = EmployeeSerializer(employees, many=True).data
        return Response(data, status=status.HTTP_200_OK)
    

class AddEmployeesAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser]

    def post(self, request, **kwargs):
        data_file = request.FILES['data_file']
        if not data_file.name.endswith('.csv'):
            error = {"message": "File is note CSV type"}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        decoded_file = data_file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)

        data_set = pd.read_csv(data_file.open()) 
        rows_count = len(data_set.axes[0]) 
        cols_count = len(data_set.axes[1]) 
        
        if rows_count <= 19 and cols_count >= 5:
            try:
                for dtl in reader:
                    employee_obj = Employee()
                    employee_instance = Employee.objects.filter(employee_code=dtl['employee-code'])
                    if not employee_instance.exists():
                        employee_obj.employee_code = dtl['employee-code']
                        employee_obj.employee_name = dtl['employee-name']
                        employee_obj.department = dtl['department']
                        employee_obj.age = int(dtl['age'])
                        employee_obj.experience = int(dtl['experience'])
                        employee_obj.save()
                return Response({"message": "Employees datas uploaded"}, status=status.HTTP_201_CREATED)
            except:
                error = {"message": "somthing went wrong!, CSV file columns heading must be 'employee-code', 'emaployee-name, 'department', 'age', 'experience'"}
                return Response(error, status=status.HTTP_400_BAD_REQUEST)
           
        else:
            error = {"message": "Incorrect file format, CSV file must have minimum 5 columns and maximum 20 rows allowed"}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

    
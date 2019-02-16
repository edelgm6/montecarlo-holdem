from django.shortcuts import render
from django.views import View
from play.models import Simulation
from play.serializers import SimulationSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

class IndexView(View):
	
	template_name = 'play/index.html'
	
	def get(self, request, *args, **kwargs):
		return render(request, self.template_name)
    
class ResultsView(APIView):
    
    def post(self, request, *args, **kwargs):
        
        print(request.data)
        serializer = SimulationSerializer(data=request.data)
        
        if serializer.is_valid():
            simulation = serializer.save()
            
            simulation.run_simulation()
            return Response(serializer.data)
        else:
            print(serializer.errors)
            return Response(serializer.errors)
        
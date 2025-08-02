# vehicles/views.py
from django.views.generic import ListView, DetailView
from .models import Vehicle, VehicleCategory
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import VehicleForm
from .models import VehicleImage
from django.shortcuts import redirect

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

@require_POST
@csrf_exempt
def like_vehicle(request, vehicle_id):
    try:
        vehicle = Vehicle.objects.get(id=vehicle_id)
        new_count = vehicle.increment_likes()
        return JsonResponse({
            'status': 'success',
            'like_count': new_count,
            'vehicle_id': vehicle_id
        })
    except Vehicle.DoesNotExist:
        return JsonResponse({'status': 'error'}, status=404)

@require_POST
@csrf_exempt
def share_vehicle(request, vehicle_id):
    try:
        vehicle = Vehicle.objects.get(id=vehicle_id)
        new_count = vehicle.increment_shares()
        return JsonResponse({
            'status': 'success', 
            'share_count': new_count,
            'vehicle_id': vehicle_id
        })
    except Vehicle.DoesNotExist:
        return JsonResponse({'status': 'error'}, status=404)

class VehicleListView(ListView):
    model = Vehicle
    template_name = 'vehicles/vehicle_list.html'
    context_object_name = 'vehicles'
    paginate_by = 12

    def get_queryset(self):
        return Vehicle.objects.filter(is_featured=True)

class VehicleDetailView(DetailView):
    model = Vehicle
    template_name = 'vehicles/vehicle_detail.html'
    context_object_name = 'vehicle'
    slug_field = 'slug'

class CategoryView(ListView):
    model = Vehicle
    template_name = 'vehicles/vehicle_list.html'
    context_object_name = 'vehicles'
    paginate_by = 12

    def get_queryset(self):
        return Vehicle.objects.filter(category__slug=self.kwargs['slug'])


class VehicleCreateView(LoginRequiredMixin, CreateView):
    model = Vehicle
    form_class = VehicleForm
    template_name = 'vehicles/vehicle_form.html'
    success_url = reverse_lazy('vehicles:vehicle_list')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        
        # Handle multiple image uploads
        if self.request.FILES.getlist('images'):
            for img in self.request.FILES.getlist('images'):
                VehicleImage.objects.create(
                    vehicle=self.object,
                    image=img
                )
        return response
# edit and delete
class VehicleEditView(LoginRequiredMixin, CreateView):
    model = Vehicle
    form_class = VehicleForm
    template_name = 'vehicles/vehicle_form.html'
    
    def get_object(self, queryset=None):
        return Vehicle.objects.get(slug=self.kwargs['slug'])

    def get_success_url(self):
        return reverse_lazy('vehicles:vehicle_detail', kwargs={'slug': self.object.slug})
class VehicleDeleteView(LoginRequiredMixin, DetailView):
    model = Vehicle
    template_name = 'vehicles/vehicle_confirm_delete.html'
    
    def get_object(self, queryset=None):
        return Vehicle.objects.get(slug=self.kwargs['slug'])

    def post(self, request, *args, **kwargs):
        vehicle = self.get_object()
        vehicle.delete()
        return redirect('vehicles:vehicle_list')
# import datetime
from audioop import reverse
from django.core.mail import send_mail
from multiprocessing import context
from django.shortcuts import render
from .models import Lead, Agent, Category
from django.views.generic import CreateView, ListView, DetailView,UpdateView, DeleteView, FormView
from django.shortcuts import reverse
# from .forms import LeadForm,
from .forms import LeadModelForm, CustomUserCreationForm, AssignAgentForm,  CategoryModelForm, LeadCategoryUpdateForm
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from agents.mixins import OrganisorAndLoginRequiredMixin


# Create your views here.

def landing_page(request):
    return render(request, "landing_page.html")


class Signupview(CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse("login")


              #   Home_page
class LeadListView(LoginRequiredMixin, ListView):
    template_name = "lead_Lists.html"
    context_object_name = "leads"

    


    
    def get_queryset(self):
        user = self.request.user
            # initial queryset of leads for the entire organisation #
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation=user.userprofile, agent__isnull=False)
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation, agent__isnull=False)
                # filter for the agent that logged in #  
            queryset = queryset.filter(agent__user=user)
        return queryset  

    def get_context_data(self, **kwargs):
        context = super(LeadListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organisor:
            queryset = Lead.objects.filter(
                organisation=user.userprofile, 
                agent__isnull=True
            ) 
            context.update({
                "unassigned_leads": queryset
            })
        return context   






# def lead_Lists(request):
#     leads = Lead.objects.all()
#     context = {
#         "leads": leads
#     }
#     return render(request, "lead_Lists.html", context) 

  

          #  details of each leads
class lead_detail(OrganisorAndLoginRequiredMixin, DetailView):
    template_name = "lead_detail.html"
    context_object_name = "lead"

    def get_queryset(self):
        user = self.request.user
            # initial queryset of leads for the entire organisation #
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation)
                # filter for the agent that logged in #  
            queryset = queryset.filter(agent__user=user)
        return queryset   



class lead_update(OrganisorAndLoginRequiredMixin, UpdateView):
    template_name = "lead_update.html"
    form_class = LeadModelForm
    
    def get_queryset(self):
       user = self.request.user
       # initial queryset of leads for the entire organisation #
       return Lead.objects.filter(organisation=user.userprofile)

    def get_success_url(self):
        return reverse("leads:lead-list")
    






class lead_delete(OrganisorAndLoginRequiredMixin, DeleteView):
    template_name = "lead-delete.html"

    
    def get_queryset(self):
       user = self.request.user
       # initial queryset of leads for the entire organisation #
       return Lead.objects.filter(organisation=user.userprofile)

    def get_success_url(self):
        return reverse("leads:lead-list")







class LeadCreateView(OrganisorAndLoginRequiredMixin, CreateView):
    template_name = "lead_create.html"
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse("leads:lead-list")
            
    def form_valid(self, form):
        lead = form.save(commit=False)
        lead.organisation = self.request.user.userprofile
        lead.save()
        # send_mail(
        #     subject="A lead as been created",
        #     message="Go to the site to see the new lead", from_email="test@test.com",
        #     recipient_list=["test2@.com"]
        #     )
        return super(LeadCreateView, self).form_valid(form)



class AssignAgentView(OrganisorAndLoginRequiredMixin, FormView):
    template_name = "assign_agent.html"
    form_class = AssignAgentForm


    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update({
            "request": self.request
        })
        return kwargs


    def get_success_url(self):
        return reverse("leads:lead-list")

    def form_valid(self, form):
        agent = (form.cleaned_data["agent"])
        lead = Lead.objects.get(id=self.kwargs["pk"])
        lead.agent = agent
        lead.save()
        return super(AssignAgentView, self).form_valid(form)

class CategoryListView(LoginRequiredMixin, ListView):
    template_name = "category_list.html"
    context_object_name = "category_list"

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        user = self.request.user

        if user.is_organisor:
            queryset = Lead.objects.filter(
                organisation=user.userprofile
            )
        else:
            queryset = Lead.objects.filter(
                organisation=user.agent.organisation
            )

        context.update({
            "unassigned_lead_count": queryset.filter(category__isnull=True).count()
        })
        return context

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        if user.is_organisor:
            queryset = Category.objects.filter(
                organisation=user.userprofile
            )
        else:
            queryset = Category.objects.filter(
                organisation=user.agent.organisation
            )
        return queryset
	

class CategoryDetailView(LoginRequiredMixin, DetailView):
    template_name = "category_detail.html"
    context_object_name = "category"

    def get_queryset(self):
        user = self.request.user
        if user.is_organisor:
            queryset = Category.objects.filter(
                organisation=user.userprofile
            )
        else:
            queryset = Category.objects.filter(
                organisation=user.agent.organisation
            )
        return queryset        			   
				  
					   
class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "category_update.html"
    form_class = CategoryModelForm
    def get_queryset(self):
       user = self.request.user
       # initial queryset of leads for the entire organisation #
       if user.is_organisor:
            queryset = Lead.objects.filter(organisation=user.userprofile)
       else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation)
                # filter for the agent that logged in #  
            queryset = queryset.filter(agent__user=user)
       return queryset  

    def get_success_url(self):
        return reverse("leads:lead-detail", kwargs={"pk": self.get_object().id})


class CategoryCreateView(OrganisorAndLoginRequiredMixin, CreateView):
    template_name = "category_create.html"
    form_class = CategoryModelForm

    def get_success_url(self):
        return reverse("leads:category-list")

    def form_valid(self, form):
        category = form.save(commit=False)
        category.organisation = self.request.user.userprofile
        category.save()
        return super(CategoryCreateView, self).form_valid(form)



class CategoryDeleteView(OrganisorAndLoginRequiredMixin, DeleteView):
    template_name = "category_delete.html"

    def get_success_url(self):
        return reverse("leads:category-list")

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        if user.is_organisor:
            queryset = Category.objects.filter(
                organisation=user.userprofile
            )
        else:
            queryset = Category.objects.filter(
                organisation=user.agent.organisation
            )
        return queryset


    
class LeadCategoryUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "lead_category_update.html"
    form_class = LeadCategoryUpdateForm

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation)
            # filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
        return queryset

    def get_success_url(self):
        return reverse("leads:lead-detail", kwargs={"pk": self.get_object().id})

    def form_valid(self, form):
        lead_before_update = self.get_object()
        instance = form.save(commit=False)
        converted_category = Category.objects.get(name="Converted")
        if form.cleaned_data["category"] == converted_category:
            # update the date at which this lead was converted
            if lead_before_update.category != converted_category:
                # this lead has now been converted
                instance.converted_date = datetime.datetime.now()
        instance.save()
        return super(LeadCategoryUpdateView, self).form_valid(form)
			    











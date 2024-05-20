from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import LabReportForm
import PyPDF2
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import os
from django.conf import settings

def process_pdf(pdf_path, header_image_path, footer_image_path, name):
    output_file_name = f'{name}_processed_lab_report.pdf'
    output_pdf_path = os.path.join(settings.DOWNLOADS_DIR, output_file_name)

    # Open the input PDF file
    with open(pdf_path, 'rb') as input_pdf_file:
        # Create a PDF reader object
        pdf_reader = PyPDF2.PdfReader(input_pdf_file)
        
        # Create a PDF writer object
        pdf_writer = PyPDF2.PdfWriter()

        # Open the header and footer images
        header_img = canvas.Canvas("header.pdf", pagesize=A4)
        header_img.drawInlineImage(header_image_path, 0, 750, width=600, height=130)
        header_img.save()

        footer_img = canvas.Canvas("footer.pdf", pagesize=A4)
        footer_img.drawInlineImage(footer_image_path, 0, 0, width=600, height=85)
        footer_img.save()

        # Iterate through each page of the input PDF
        for page_num in range(len(pdf_reader.pages)):
            # Get the page object
            page = pdf_reader.pages[page_num]

            # Merge header and footer to the page
            header_page = PyPDF2.PdfReader("header.pdf")
            footer_page = PyPDF2.PdfReader("footer.pdf")

            page.merge_page(header_page.pages[0])
            page.merge_page(footer_page.pages[0])

            # Add the modified page to the PDF writer
            pdf_writer.add_page(page)

    # Save the output PDF
    with open(output_pdf_path, 'wb') as output_pdf_file:
        pdf_writer.write(output_pdf_file)

    return output_pdf_path

def process_lab_report(request):
    if request.method == 'POST':
        form = LabReportForm(request.POST, request.FILES)
        if form.is_valid():
            lab_report = form.save()


            print("Lab Report created:", lab_report)

            # Get the name entered in the form
            name = form.cleaned_data['name'] 

            # Specify paths to header and footer images
            header_image_path = os.path.join(settings.STATIC_ROOT, 'reportspdf/images/GABRIELDIAGNOSTICS.png')
            footer_image_path = os.path.join(settings.STATIC_ROOT, 'reportspdf/images/FOOTER.png')
            

            # Debug print to check paths
            print("Header image path:", header_image_path)
            print("Footer image path:", footer_image_path)

            print("LabReport object created successfully:", lab_report)  # Add this debug print



            # Process the lab report PDF
            output_pdf_path = process_pdf(
                lab_report.pdf_file.path, header_image_path, footer_image_path, name
            )



            print("Output PDF path:", output_pdf_path)  # Add this debug print

            # Provide the processed PDF for download
            with open(output_pdf_path, 'rb') as pdf_file:
                response = HttpResponse(pdf_file.read(), content_type='application/pdf')
                response['Content-Disposition'] = f'attachment; filename={name}_lab_report.pdf'
                return response
    else:
        form = LabReportForm()

    return render(request, 'overlay-pdf.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('process_lab_report')  # Redirect to dashboard if user is already logged in

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('process_lab_report')  # Redirect to the dashboard page after login
        else:
            error_message = "Invalid username or password. Please try again."
            return render(request, 'login.html', {'error_message': error_message})
    return render(request, 'login.html')


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')  # Redirect to the login page after logout

import os
import glob
import json
import subprocess
import psutil
from datetime import datetime
from flask import Flask, send_file, jsonify, request, send_from_directory, render_template, flash, redirect, url_for

# Configure app
app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.secret_key = os.environ.get('SECRET_KEY', 'hrim_wellness_secret_key')

# Root directory of the project
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def index():
    """Serve the dashboard HTML file"""
    return render_template('dashboard.html')

@app.route('/favicon.ico')
def favicon():
    """Serve the favicon"""
    return send_from_directory(os.path.join(app.root_path, 'static'),
                             'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/api/test_pdf-1')
def test_pdf_1():
    """Test endpoint for PDF generation - step 1"""
    return jsonify({
        'status': 'success',
        'message': 'PDF test endpoint 1 working'
    })

@app.route('/api/test_pdf-3')
def test_pdf_3():
    """Test endpoint for PDF generation - step 3"""
    return jsonify({
        'status': 'success',
        'message': 'PDF test endpoint 3 working'
    })

@app.route('/api/ngrok-1')
def ngrok_1():
    """Test endpoint for ngrok setup - step 1"""
    return jsonify({
        'status': 'success',
        'message': 'Ngrok test endpoint working'
    })

@app.route('/api/status')
def get_status():
    """Get the status of all services"""
    services = {
        'automation_workflow': is_process_running('automate_workflow.py'),
        'whatsapp_chatbot': is_process_running('whatsapp_chatbot.py'),
        'pdf_generation': check_pdf_generation()
    }
    return jsonify(services)

@app.route('/api/run', methods=['POST'])
def run_command():
    """Run a command"""
    command = request.json.get('command')
    if not command:
        return jsonify({'error': 'No command provided'}), 400
    
    try:
        # Run the command as a background process
        subprocess.Popen(command.split(), 
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE)
        return jsonify({'status': 'success', 'message': f'Command {command} started'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/stop', methods=['POST'])
def stop_service():
    """Stop a service"""
    service = request.json.get('service')
    if not service:
        return jsonify({'error': 'No service provided'}), 400
    
    try:
        # Find and kill the process
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if service in ' '.join(proc.info['cmdline'] or []):
                    proc.kill()
                    return jsonify({'status': 'success', 'message': f'Service {service} stopped'})
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        
        return jsonify({'status': 'error', 'message': f'Service {service} not found'}), 404
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/pdfs')
def get_pdfs():
    """Get a list of generated PDFs"""
    pdf_dir = os.path.join(ROOT_DIR, 'generated_pdfs')
    if not os.path.exists(pdf_dir):
        os.makedirs(pdf_dir)
    
    pdfs = []
    for pdf_file in glob.glob(os.path.join(pdf_dir, '*.pdf')):
        filename = os.path.basename(pdf_file)
        created_time = datetime.fromtimestamp(os.path.getctime(pdf_file))
        size = os.path.getsize(pdf_file)
        pdfs.append({
            'filename': filename,
            'created': created_time.strftime('%Y-%m-%d %H:%M:%S'),
            'size': f"{size / 1024:.1f} KB",
            'path': f"generated_pdfs/{filename}"
        })
    
    # Sort by creation time, newest first
    pdfs.sort(key=lambda x: x['created'], reverse=True)
    return jsonify(pdfs)

@app.route('/api/logs')
def get_logs():
    """Get system logs"""
    # This is a simplified implementation
    # In a real app, you would read from actual log files
    logs = [
        f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] INFO: Dashboard server started",
        f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] INFO: Automation workflow status: {'running' if is_process_running('automate_workflow.py') else 'stopped'}",
        f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] INFO: WhatsApp chatbot status: {'running' if is_process_running('whatsapp_chatbot.py') else 'stopped'}"
    ]
    return jsonify(logs)

@app.route('/api/test_pdf', methods=['POST'])
def test_pdf():
    """Test PDF generation"""
    try:
        # Create a simple test PDF
        test_content = "# Test Wellness Plan\n\nThis is a test wellness plan generated to verify PDF functionality."
        test_user = {
            "Full Name": "Test User",
            "Email": "test@example.com",
            "WhatsApp Contact Number": "+91 9876543210"
        }
        
        # Import the PDF generation function
        from generate_pdf import create_pdf
        
        # Generate the test PDF
        pdf_path = create_pdf(test_content, test_user, "test_wellness_plan.pdf")
        
        if pdf_path:
            return jsonify({
                'status': 'success', 
                'message': 'PDF generated successfully',
                'path': pdf_path
            })
        else:
            return jsonify({
                'status': 'error', 
                'message': 'Failed to generate PDF'
            }), 500
    except Exception as e:
        return jsonify({
            'status': 'error', 
            'message': f'Error generating PDF: {str(e)}'
        }), 500

@app.route('/api/ngrok', methods=['POST'])
def setup_ngrok():
    """Set up ngrok tunnel"""
    try:
        # Check if ngrok is installed
        ngrok_path = subprocess.check_output(['where', 'ngrok'], 
                                           stderr=subprocess.STDOUT).decode().strip()
        
        # Start ngrok in a background process
        subprocess.Popen([ngrok_path, 'http', '5000'], 
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE)
        
        # Wait a moment for ngrok to start
        import time
        time.sleep(2)
        
        # Get the public URL
        try:
            ngrok_info = subprocess.check_output(['curl', 'http://localhost:4040/api/tunnels'], 
                                               stderr=subprocess.STDOUT).decode()
            ngrok_data = json.loads(ngrok_info)
            public_url = ngrok_data['tunnels'][0]['public_url']
            
            return jsonify({
                'status': 'success',
                'webhook_url': f"{public_url}/whatsapp"
            })
        except:
            return jsonify({
                'status': 'error',
                'message': 'Ngrok started but could not retrieve public URL'
            }), 500
    except subprocess.CalledProcessError:
        return jsonify({
            'status': 'error',
            'message': 'Ngrok not found. Please install ngrok first.'
        }), 500
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error setting up ngrok: {str(e)}'
        }), 500

def is_process_running(process_name):
    """Check if a process is running by name"""
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if process_name in ' '.join(proc.info['cmdline'] or []):
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def check_pdf_generation():
    """Check if PDF generation is working"""
    try:
        # Import the PDF generation module
        import generate_pdf
        return True
    except Exception:
        return False

@app.route('/wellness_form')
def wellness_form():
    """Render the wellness form page"""
    return render_template('wellness_form.html')

@app.route('/generate_wellness_plan', methods=['POST'])
def generate_wellness_plan():
    """Generate a wellness plan from form data"""
    try:
        # Extract form data
        form_data = {}
        for key in request.form:
            if key == 'health_goals':
                # Handle multiple checkboxes for health goals
                form_data['Primary Health Goals'] = ', '.join(request.form.getlist('health_goals'))
            else:
                form_data[key] = request.form.get(key)
        
        # Import the wellness plan generator
        from app.core.wellness.generate_wellness_pdf import process_form_data
        
        # Generate the wellness plan
        output_path = process_form_data(form_data)
        
        if output_path:
            # Extract filename from path
            filename = os.path.basename(output_path)
            
            # Check if it's a PDF
            if output_path.endswith('.pdf'):
                return send_file(output_path, 
                                 mimetype='application/pdf',
                                 as_attachment=True,
                                 download_name=filename)
            else:
                # Render the markdown content
                with open(output_path, 'r', encoding='utf-8') as f:
                    markdown_content = f.read()
                
                return render_template('wellness_result.html', 
                                      content=markdown_content,
                                      client_name=form_data.get('Full Name', 'Anonymous'),
                                      download_path=output_path)
        else:
            # Handle error
            flash("Failed to generate wellness plan. Please try again.", "error")
            return redirect(url_for('wellness_form'))
    
    except Exception as e:
        app.logger.error(f"Error generating wellness plan: {str(e)}")
        flash(f"An error occurred: {str(e)}", "error")
        return redirect(url_for('wellness_form'))

@app.route('/download/<path:filename>')
def download_file(filename):
    """Download a generated file"""
    # Get the generated data path
    output_dir = os.environ.get('GENERATED_DATA_PATH', 'generated_data')
    
    # Check if the file exists in the output directory
    file_path = os.path.join(output_dir, filename)
    if os.path.exists(file_path):
        # Determine the MIME type
        if filename.endswith('.pdf'):
            mimetype = 'application/pdf'
        elif filename.endswith('.md'):
            mimetype = 'text/markdown'
        else:
            mimetype = 'application/octet-stream'
        
        return send_file(file_path, 
                         mimetype=mimetype,
                         as_attachment=True,
                         download_name=filename)
    else:
        flash(f"File {filename} not found", "error")
        return redirect(url_for('index'))

# API endpoints for wellness plans
@app.route('/wellness_dashboard')
def wellness_dashboard():
    """Render the wellness dashboard page"""
    return render_template('wellness_dashboard.html')

@app.route('/api/wellness-plans')
def get_wellness_plans():
    """Get a list of generated wellness plans"""
    output_dir = os.environ.get('GENERATED_DATA_PATH', 'generated_data')
    plans = []
    
    try:
        if not os.path.exists(output_dir):
            return jsonify([])
        
        # Get all markdown files in the output directory
        for filename in os.listdir(output_dir):
            if filename.endswith('.md'):
                file_path = os.path.join(output_dir, filename)
                stats = os.stat(file_path)
                file_size = stats.st_size / 1024  # KB
                creation_time = datetime.fromtimestamp(stats.st_ctime)
                
                # Extract client name from filename
                name_parts = filename.split('_')
                if len(name_parts) >= 3 and name_parts[0] == 'wellness' and name_parts[1] == 'plan':
                    client_name = ' '.join(name_parts[2:-2])
                else:
                    client_name = filename
                
                plans.append({
                    'name': client_name,
                    'path': file_path,
                    'date': creation_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'type': 'Markdown',
                    'size': f'{file_size:.2f} KB'
                })
        
        # Sort by creation date, newest first
        plans.sort(key=lambda x: x['date'], reverse=True)
        
        return jsonify(plans)
    except Exception as e:
        app.logger.error(f"Error getting wellness plans: {str(e)}")
        return jsonify([])

@app.route('/api/wellness-plan')
def get_wellness_plan():
    """Get the content of a wellness plan"""
    plan_path = request.args.get('path')
    
    if not plan_path or not os.path.exists(plan_path):
        return "Plan not found", 404
    
    try:
        with open(plan_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except Exception as e:
        app.logger.error(f"Error reading wellness plan: {str(e)}")
        return f"Error reading plan: {str(e)}", 500

@app.route('/api/generate-random', methods=['POST'])
def api_generate_random():
    """Generate a wellness plan with random data"""
    try:
        # Import the necessary modules
        from app.api.cohere_integration import set_test_api_key
        from tests.generate_test_wellness_plan import generate_random_form_data
        
        # Set the Cohere API key
        test_api_key = "q9OWktdIYYibhnyQTp1hiAhNwUWg9pvrHI9moYlh"
        set_test_api_key(test_api_key)
        
        # Get the output format
        data = request.json
        output_format = data.get('format', 'markdown')
        
        # Generate random form data
        form_data = generate_random_form_data()
        
        # Generate the wellness plan
        output_path = None
        if output_format == 'pdf':
            # Import the PDF generation function
            try:
                from app.core.wellness.generate_wellness_pdf import process_form_data
                output_path = process_form_data(form_data)
            except ImportError:
                # Fall back to markdown
                from app.api.cohere_integration import generate_wellness_plan
                wellness_plan = generate_wellness_plan(form_data)
                
                # Save the markdown file
                output_dir = os.environ.get('GENERATED_DATA_PATH', 'generated_data')
                os.makedirs(output_dir, exist_ok=True)
                
                user_name = form_data.get('Full Name', 'anonymous').replace(' ', '_')
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_filename = f"wellness_plan_{user_name}_{timestamp}.md"
                output_path = os.path.join(output_dir, output_filename)
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(wellness_plan)
        else:
            # Just generate the markdown
            from app.api.cohere_integration import generate_wellness_plan
            wellness_plan = generate_wellness_plan(form_data)
            
            # Save the markdown file
            output_dir = os.environ.get('GENERATED_DATA_PATH', 'generated_data')
            os.makedirs(output_dir, exist_ok=True)
            
            user_name = form_data.get('Full Name', 'anonymous').replace(' ', '_')
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"wellness_plan_{user_name}_{timestamp}.md"
            output_path = os.path.join(output_dir, output_filename)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(wellness_plan)
        
        # Return the result
        if output_path:
            return jsonify({
                'success': True,
                'message': f"Wellness plan generated successfully for {form_data.get('Full Name', 'anonymous')}",
                'planPath': output_path
            })
        else:
            return jsonify({
                'success': False,
                'message': "Failed to generate wellness plan"
            })
    except Exception as e:
        app.logger.error(f"Error generating wellness plan: {str(e)}")
        return jsonify({
            'success': False,
            'message': f"Error: {str(e)}"
        })

@app.route('/api/generate-from-file', methods=['POST'])
def api_generate_from_file():
    """Generate a wellness plan from a JSON file"""
    try:
        # Import the necessary modules
        from app.api.cohere_integration import set_test_api_key, generate_wellness_plan
        
        # Set the Cohere API key
        test_api_key = "q9OWktdIYYibhnyQTp1hiAhNwUWg9pvrHI9moYlh"
        set_test_api_key(test_api_key)
        
        # Get the input file path and output format
        data = request.json
        file_path = data.get('filePath')
        output_format = data.get('format', 'markdown')
        
        if not file_path:
            return jsonify({
                'success': False,
                'message': "No file path provided"
            })
        
        # Load the form data from the file
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                form_data = json.load(f)
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f"Error loading file: {str(e)}"
            })
        
        # Generate the wellness plan
        output_path = None
        if output_format == 'pdf':
            # Import the PDF generation function
            try:
                from app.core.wellness.generate_wellness_pdf import process_form_data
                output_path = process_form_data(form_data)
            except ImportError:
                # Fall back to markdown
                wellness_plan = generate_wellness_plan(form_data)
                
                # Save the markdown file
                output_dir = os.environ.get('GENERATED_DATA_PATH', 'generated_data')
                os.makedirs(output_dir, exist_ok=True)
                
                user_name = form_data.get('Full Name', 'anonymous').replace(' ', '_')
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_filename = f"wellness_plan_{user_name}_{timestamp}.md"
                output_path = os.path.join(output_dir, output_filename)
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(wellness_plan)
        else:
            # Just generate the markdown
            wellness_plan = generate_wellness_plan(form_data)
            
            # Save the markdown file
            output_dir = os.environ.get('GENERATED_DATA_PATH', 'generated_data')
            os.makedirs(output_dir, exist_ok=True)
            
            user_name = form_data.get('Full Name', 'anonymous').replace(' ', '_')
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"wellness_plan_{user_name}_{timestamp}.md"
            output_path = os.path.join(output_dir, output_filename)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(wellness_plan)
        
        # Return the result
        if output_path:
            return jsonify({
                'success': True,
                'message': f"Wellness plan generated successfully for {form_data.get('Full Name', 'anonymous')}",
                'planPath': output_path
            })
        else:
            return jsonify({
                'success': False,
                'message': "Failed to generate wellness plan"
            })
    except Exception as e:
        app.logger.error(f"Error generating wellness plan: {str(e)}")
        return jsonify({
            'success': False,
            'message': f"Error: {str(e)}"
        })

if __name__ == '__main__':
    # Create static directory if it doesn't exist
    static_dir = os.path.join(app.root_path, 'static')
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)
    
    # Create an empty favicon.ico if it doesn't exist
    favicon_path = os.path.join(static_dir, 'favicon.ico')
    if not os.path.exists(favicon_path):
        with open(favicon_path, 'wb') as f:
            f.write(b'')
    
    app.run(host='0.0.0.0', port=8080, debug=True) 
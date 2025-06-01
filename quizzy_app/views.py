from django.shortcuts import render, redirect,  get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import IntegerField
from django.db.models.functions import Cast
from django.http import HttpResponse
from .models import *
import ast
import json
from .encryptor import  *
from .manager import *
from .uploader import *
from .converter import *
from .corrector import *  
from .corrector_2 import *
from .corrector_3 import *
from .corrector_4 import *
from .latex import *
from .latex_2 import *
from .latex_3 import *
from .scorer import *
import html

def index(request):
  return render(request, "quizzy/index.html")  

def zohoverify(request):
  return render(request, "quizzy/verifyforzoho.html")  

def bridge(request):
   quizz_Id = request.GET.get('id')
   id = encrypt_data(str(quizz_Id))
   return redirect(f'/editor?session={id}')

def bridge2(request):
   quizz_Id = request.GET.get('id')
   id = encrypt_data_2(str(quizz_Id))
   return redirect(f'/quiz?session={id}')

def mytree(request):
    Encrypted_Tree_id = request.GET.get('session')
    password = request.GET.get('password')
    path = request.GET.get('path', '/')
    folderId = request.GET.get('folderId', 'root')
    allowEdit = request.GET.get('allowEdit', '0') == '1'

    if not Encrypted_Tree_id:
        return redirect('/')

    try:
        # Handle both encrypted and plain user IDs
        if isinstance(Encrypted_Tree_id, str):
            # First decode HTML entities if present
            import html
            html_decoded = html.unescape(Encrypted_Tree_id)

            # Then URL decode
            import urllib.parse
            url_decoded = urllib.parse.unquote(html_decoded)

            # Now try to extract the encrypted data
            if url_decoded.startswith("b'") and url_decoded.endswith("'"):
                # Remove b' and ' wrapper
                clean_data = url_decoded[2:-1]
                Actual_Tree_id = decrypt_data(clean_data.encode())
            elif url_decoded.startswith('b"') and url_decoded.endswith('"'):
                # Remove b" and " wrapper  
                clean_data = url_decoded[2:-1]
                Actual_Tree_id = decrypt_data(clean_data.encode())
            else:
                # Try direct decryption
                Actual_Tree_id = decrypt_data(url_decoded.encode())
        else:
            Actual_Tree_id = decrypt_data(Encrypted_Tree_id)
    except Exception as e:
        print(f"Decryption error: {e}")
        print(f"Original session: {Encrypted_Tree_id}")
        # Try one more fallback approach
        try:
            import html
            import urllib.parse

            # Multiple decode attempts
            decoded = html.unescape(str(Encrypted_Tree_id))
            decoded = urllib.parse.unquote(decoded)

            # Remove various possible wrappers
            if decoded.startswith("b'") and decoded.endswith("'"):
                decoded = decoded[2:-1]
            elif decoded.startswith('b"') and decoded.endswith('"'):
                decoded = decoded[2:-1]

            Actual_Tree_id = decrypt_data(decoded.encode())
        except:
            return redirect('/')

    # Check if this tree requires a password
    tree_password = request.session.get(f'tree_password_{Actual_Tree_id}')
    if tree_password and not password:
        return render(request, "quizzy/mytree_password.html", {
            'session': Encrypted_Tree_id,
            'path': path,
            'folderId': folderId,
            'allowEdit': allowEdit
        })
    elif tree_password and password != tree_password:
        return render(request, "quizzy/mytree_password.html", {
            'session': Encrypted_Tree_id,
            'path': path,
            'folderId': folderId,
            'allowEdit': allowEdit,
            'error': 'Invalid password'
        })

    # Check if invite link is protected (only when not in edit mode)
    if not allowEdit:
        invite_password = request.session.get(f'invite_password_{Actual_Tree_id}')
        if invite_password and not password:
            return render(request, "quizzy/mytree_password.html", {
                'session': Encrypted_Tree_id,
                'path': path,
                'folderId': folderId,
                'allowEdit': allowEdit,
                'is_invite_lock': True
            })
        elif invite_password and password != invite_password:
            return render(request, "quizzy/mytree_password.html", {
                'session': Encrypted_Tree_id,
                'path': path,
                'folderId': folderId,
                'allowEdit': allowEdit,
                'error': 'Invalid password',
                'is_invite_lock': True
            })

    # Fetch quizzes owned by the user
    User_Quizs = Quizz.objects.filter(Owner_id=Actual_Tree_id)
    User_Folders = Folders.objects.filter(Owner_id=Actual_Tree_id)
    Quizs = []
    Folder = []

    for User_Folder_fetch in User_Folders:
        Folder.append([
            str(User_Folder_fetch.id),
            User_Folder_fetch.Folder_Name,
            str(User_Folder_fetch.Parent_folder_id)
        ])

    for User_Quizs_fetch in User_Quizs:
        Quizs.append([
            encrypt_data(str(User_Quizs_fetch.id)),
            User_Quizs_fetch.Title,
            encrypt_data_2(str(User_Quizs_fetch.id)),
            str(User_Quizs_fetch.Parent_folder_id)
        ])

    def get_full_file_system(owner_id):
        # Fetch all folders for the owner
        folders = Folders.objects.filter(Owner_id=owner_id)

        # Fetch all quizzes for the owner
        quizzes = Quizz.objects.filter(Owner_id=owner_id)

        # Initialize file system dictionary
        file_system = {
            '/': {
                'type': 'folder',
                'id': 'root',
                'children': {},
            }
        }

        # Create a mapping of folder IDs to their details
        folder_map = {}
        for folder in folders:
            has_password = f'folder_password_{folder.id}' in request.session if hasattr(request, 'session') else False
            folder_map[folder.id] = {
                'type': 'folder', 
                'id': str(folder.id), 
                'name': html.escape(folder.Folder_Name),
                'children': {},
                'protected': has_password
            }

        # Function to generate globally unique names
        def generate_globally_unique_name(name, file_system):
            def is_name_exists(obj, check_name):
                for key, child in obj['children'].items():
                    if key == check_name:
                        return True
                    if child['type'] == 'folder' and is_name_exists(child, check_name):
                        return True
                return False

            unique_name = name
            counter = 1

            # Check name existence in entire file system starting from root
            while is_name_exists(file_system['/'], unique_name):
                unique_name = f"{name} ({counter})"
                counter += 1

            return unique_name

        # Build the folder hierarchy with unique names
        for folder in folders:
            # Determine parent
            if folder.Parent_folder_id == 'root':
                # Generate globally unique name for root-level folder
                unique_name = generate_globally_unique_name(folder.Folder_Name, file_system)

                # Update folder map and file system
                folder_map[folder.id]['name'] = unique_name
                file_system['/']['children'][unique_name] = folder_map[folder.id]
            else:
                try:
                    parent_id = int(folder.Parent_folder_id)
                    if parent_id in folder_map:
                        parent = folder_map[parent_id]

                        # Generate globally unique name 
                        unique_name = generate_globally_unique_name(folder.Folder_Name, file_system)

                        # Update folder map and parent's children
                        folder_map[folder.id]['name'] = unique_name
                        parent['children'][unique_name] = folder_map[folder.id]
                except (ValueError, KeyError):
                    pass

        # Add quizzes to their respective folders with unique names
        for quiz in quizzes:
            quiz_details = {
                'type': 'file',
                'id': str(quiz.id),
                'name': html.escape(quiz.Title),
                'crypt_id': encrypt_data_2(str(quiz.id)).decode('utf-8')
            }

            if quiz.Parent_folder_id == 'root':
                # Generate globally unique name for root-level quiz
                unique_name = generate_globally_unique_name(quiz.Title, file_system)

                # Update quiz details and file system
                quiz_details['name'] = unique_name
                file_system['/']['children'][unique_name] = quiz_details
            else:
                try:
                    parent_id = int(quiz.Parent_folder_id)
                    if parent_id in folder_map:
                        parent = folder_map[parent_id]

                        # Generate globally unique name 
                        unique_name = generate_globally_unique_name(quiz.Title, file_system)

                        # Update quiz details and parent's children
                        quiz_details['name'] = unique_name
                        parent['children'][unique_name] = quiz_details
                except (ValueError, KeyError):
                    pass

        return file_system

    Tree = get_full_file_system(Actual_Tree_id)

    # Handle all POST requests
    if request.method == 'POST':
        # Password protection requests
        set_password = request.POST.get('set_password')
        remove_password = request.POST.get('remove_password')
        folder_password = request.POST.get('folder_password')
        unlock_folder = request.POST.get('unlock_folder')
        folder_id = request.POST.get('folder_id')
        invite_password = request.POST.get('invite_password')
        remove_invite_lock = request.POST.get('remove_invite_lock')

        # File/Folder management requests
        New_Folder_Name_Post = request.POST.get('Folder_Name')
        New_Folder_Parent_Post = request.POST.get('Parent_Id')
        New_new_Folder_Name_Post = request.POST.get('Folder_New_Name')
        New_new_Folder_Id = request.POST.get('Folder_to_change_id')
        New_parent_of_draged_folder_id = request.POST.get('New_parent')
        Folder_draged_id = request.POST.get('Folder_draged_id')
        File_or_Folder = request.POST.get('isFile')
        New_Quizz_Title = request.POST.get('New_Quizz_Title')
        Parent_Quizz_Folder = request.POST.get('Parent_Quizz_Folder')
        Folder_To_Delete_ID = request.POST.get('Folder_to_Delete')

        def delete_folder(Folder_To_Delete_Id):
            InFolder_Folders = Folders.objects.filter(Parent_folder_id=Folder_To_Delete_Id) 
            InFolder_Folders.delete()
            InFolder_Quizzs = Quizz.objects.filter(Parent_folder_id=Folder_To_Delete_Id) 
            InFolder_Quizzs.delete()
            Actual_Folder = Folders.objects.get(id=int(Folder_To_Delete_Id))
            Actual_Folder.delete()

        def update_folder_parent(Draged_Folder_Id, New_parent_id, FileOrFolder):
            if str(FileOrFolder) == "0":
                new_folder_parent = Folders.objects.get(id=Draged_Folder_Id)
                new_folder_parent.Parent_folder_id = New_parent_id
                new_folder_parent.save()
            else:
                new_quiz_parent = Quizz.objects.get(id=Draged_Folder_Id)
                new_quiz_parent.Parent_folder_id = New_parent_id
                new_quiz_parent.save()

        def rename_folder(Folder_Id, Folder_New_Name):
            new_folder_name = Folders.objects.get(id=Folder_Id)
            new_folder_name.Folder_Name = Folder_New_Name
            new_folder_name.save()

        def rename_quiz(Quiz_Id, Quiz_New_Name):
            quiz = Quizz.objects.get(id=Quiz_Id)
            quiz.Title = Quiz_New_Name
            quiz.save()

        def create_folder(New_Folder_Name, New_Folder_Parent):
            new_folder = Folders(
                Owner_id=Actual_Tree_id,
                Folder_Name=New_Folder_Name,
                Parent_folder_id=New_Folder_Parent
            )
            new_folder.save()
            return new_folder.id

        def create_quiz(Quiz_Title, Parent_Folder):
            new_quizz = Quizz(
                Owner_id=Actual_Tree_id,
                Title=Quiz_Title,
                Parent_folder_id=Parent_Folder,
                Settings=['EMPTY']
            )
            new_quizz.save()

            # Create a default question for the new quiz
            default_question = Question(
                Quizz_id=str(new_quizz.id),
                Content='Enter your first question ...',
                Scoring='1',
                Order='1'
            )
            default_question.save()

            return new_quizz.id

        # Handle password protection
        if folder_password and folder_id:
            request.session[f'folder_password_{folder_id}'] = folder_password
            return JsonResponse({'status': 'folder_password_set'})
        elif unlock_folder and folder_id:
            if f'folder_password_{folder_id}' in request.session:
                del request.session[f'folder_password_{folder_id}']
            return JsonResponse({'status': 'folder_unlocked'})
        elif set_password:
            request.session[f'tree_password_{Actual_Tree_id}'] = set_password
            return JsonResponse({'status': 'password_set'})
        elif remove_password:
            if f'tree_password_{Actual_Tree_id}' in request.session:
                del request.session[f'tree_password_{Actual_Tree_id}']
            return JsonResponse({'status': 'password_removed'})
        elif invite_password:
            request.session[f'invite_password_{Actual_Tree_id}'] = invite_password
            return JsonResponse({'status': 'invite_locked'})
        elif remove_invite_lock:
            if f'invite_password_{Actual_Tree_id}' in request.session:
                del request.session[f'invite_password_{Actual_Tree_id}']
            return JsonResponse({'status': 'invite_unlocked'})

        # Handle file/folder operations
        if New_Folder_Name_Post and New_Folder_Parent_Post:
            folder_id = create_folder(New_Folder_Name_Post, New_Folder_Parent_Post)
            return JsonResponse({'New_Folder': str(folder_id)})

        if New_new_Folder_Name_Post and New_new_Folder_Id:
            try:
                # Check if it's a folder or quiz
                if Folders.objects.filter(id=New_new_Folder_Id).exists():
                    rename_folder(New_new_Folder_Id, New_new_Folder_Name_Post)
                elif Quizz.objects.filter(id=New_new_Folder_Id).exists():
                    rename_quiz(New_new_Folder_Id, New_new_Folder_Name_Post)
                return JsonResponse({'status': 'renamed'})
            except:
                return JsonResponse({'status': 'error'})

        if New_parent_of_draged_folder_id and Folder_draged_id and File_or_Folder:
            try:
                update_folder_parent(Folder_draged_id, New_parent_of_draged_folder_id, File_or_Folder)
                return JsonResponse({'status': 'moved'})
            except:
                return JsonResponse({'status': 'error'})

        if Folder_To_Delete_ID:
            try:
                # Check if it's a folder or quiz
                if Folders.objects.filter(id=Folder_To_Delete_ID).exists():
                    delete_folder(Folder_To_Delete_ID)
                elif Quizz.objects.filter(id=Folder_To_Delete_ID).exists():
                    quiz_to_delete = Quizz.objects.get(id=Folder_To_Delete_ID)
                    # Delete associated questions and choices
                    Question.objects.filter(Quizz_id=Folder_To_Delete_ID).delete()
                    Choice.objects.filter(Quizz_id=Folder_To_Delete_ID).delete()
                    quiz_to_delete.delete()
                return JsonResponse({'status': 'deleted'})
            except:
                return JsonResponse({'status': 'error'})

        if New_Quizz_Title and Parent_Quizz_Folder:
            try:
                quiz_id = create_quiz(New_Quizz_Title, Parent_Quizz_Folder)
                return JsonResponse({'ID': str(quiz_id)})
            except:
                return JsonResponse({'status': 'error'})

    return render(request, "quizzy/mytree.html", {
        'Tree_JSON': json.dumps(Tree),
        'path': path,
        'folderId': folderId,
        'allowEdit': allowEdit,
        'has_password': f'tree_password_{Actual_Tree_id}' in request.session,
        'invite_locked': f'invite_password_{Actual_Tree_id}' in request.session
    })


@login_required
def dashboard(request):
    # Fetch quizzes owned by the logged-in user
    User_Quizs = Quizz.objects.filter(Owner_id=request.user.id)
    User_Folders = Folders.objects.filter(Owner_id=request.user.id)
    Quizs = []
    Folder = []

    for User_Folder_fetch in User_Folders:
        Folder.append([
            str(User_Folder_fetch.id),
            User_Folder_fetch.Folder_Name,
            str(User_Folder_fetch.Parent_folder_id)
        ])

    for User_Quizs_fetch in User_Quizs:
        Quizs.append([
            encrypt_data(str(User_Quizs_fetch.id)),
            User_Quizs_fetch.Title,
            encrypt_data_2(str(User_Quizs_fetch.id)),
            str(User_Quizs_fetch.Parent_folder_id)
        ])

    def get_full_file_system(owner_id):
        # Fetch all folders for the owner
        folders = Folders.objects.filter(Owner_id=owner_id)

        # Fetch all quizzes for the owner
        quizzes = Quizz.objects.filter(Owner_id=owner_id)

        # Initialize file system dictionary
        file_system = {
            '/': {
                'type': 'folder',
                'id': 'root',
                'children': {},
            }
        }

        # Create a mapping of folder IDs to their details
        folder_map = {}
        for folder in folders:
            has_password = f'folder_password_{folder.id}' in request.session if hasattr(request, 'session') else False
            folder_map[folder.id] = {
                'type': 'folder', 
                'id': str(folder.id), 
                'name': html.escape(folder.Folder_Name),
                'children': {},
                'protected': has_password
            }

        # Function to generate globally unique names
        def generate_globally_unique_name(name, file_system):
            def is_name_exists(obj, check_name):
                for key, child in obj['children'].items():
                    if key == check_name:
                        return True
                    if child['type'] == 'folder' and is_name_exists(child, check_name):
                        return True
                return False

            unique_name = name
            counter = 1

            # Check name existence in entire file system starting from root
            while is_name_exists(file_system['/'], unique_name):
                unique_name = f"{name} ({counter})"
                counter += 1

            return unique_name

        # Build the folder hierarchy with unique names
        for folder in folders:
            # Determine parent
            if folder.Parent_folder_id == 'root':
                # Generate globally unique name for root-level folder
                unique_name = generate_globally_unique_name(folder.Folder_Name, file_system)

                # Update folder map and file system
                folder_map[folder.id]['name'] = unique_name
                file_system['/']['children'][unique_name] = folder_map[folder.id]
            else:
                try:
                    parent_id = int(folder.Parent_folder_id)
                    if parent_id in folder_map:
                        parent = folder_map[parent_id]

                        # Generate globally unique name 
                        unique_name = generate_globally_unique_name(folder.Folder_Name, file_system)

                        # Update folder map and parent's children
                        folder_map[folder.id]['name'] = unique_name
                        parent['children'][unique_name] = folder_map[folder.id]
                except (ValueError, KeyError):
                    pass

        # Add quizzes to their respective folders with unique names
        for quiz in quizzes:
            quiz_details = {
                'type': 'file',
                'id': str(quiz.id),
                'name': html.escape(quiz.Title)
            }

            if quiz.Parent_folder_id == 'root':
                # Generate globally unique name for root-level quiz
                unique_name = generate_globally_unique_name(quiz.Title, file_system)

                # Update quiz details and file system
                quiz_details['name'] = unique_name
                file_system['/']['children'][unique_name] = quiz_details
            else:
                try:
                    parent_id = int(quiz.Parent_folder_id)
                    if parent_id in folder_map:
                        parent = folder_map[parent_id]

                        # Generate globally unique name 
                        unique_name = generate_globally_unique_name(quiz.Title, file_system)

                        # Update quiz details and parent's children
                        quiz_details['name'] = unique_name
                        parent['children'][unique_name] = quiz_details
                except (ValueError, KeyError):
                    pass

        return file_system

    Tree = get_full_file_system(request.user.id)

    # Check for user's subscription
    Get_User_Subscription = Subscriptions.objects.filter(Owner_id=request.user.id)

    if Get_User_Subscription.exists():
        Active = True  
    else:
        Active = False

    if request.method == 'POST':

        New_Folder_Name_Post = request.POST.get('Folder_Name')
        New_Folder_Parent_Post = request.POST.get('Parent_Id')

        New_new_Folder_Name_Post = request.POST.get('Folder_New_Name')
        New_new_Folder_Id = request.POST.get('Folder_to_change_id')

        New_parent_of_draged_folder_id = request.POST.get('New_parent')
        Folder_draged_id = request.POST.get('Folder_draged_id')
        File_or_Folder = request.POST.get('isFile')

        New_Quizz_Title = request.POST.get('New_Quizz_Title')
        Parent_Quizz_Folder = request.POST.get('Parent_Quizz_Folder')

        Folder_To_Delete_ID = request.POST.get('Folder_to_Delete')

        def delete_folder(Folder_To_Delete_Id):
          InFolder_Folders = Folders.objects.filter(Parent_folder_id=Folder_To_Delete_Id) 
          InFolder_Folders.delete()
          InFolder_Quizzs = Quizz.objects.filter(Parent_folder_id=Folder_To_Delete_Id) 
          InFolder_Quizzs.delete()
          Actual_Folder = Folders.objects.get(id=int(Folder_To_Delete_Id))
          Actual_Folder.delete()

        def update_folder_parent(Draged_Folder_Id, New_parent_id, FileOrFolder):
              if str(FileOrFolder) == "0" :
                new_folder_parent = Folders.objects.get(id=Draged_Folder_Id)
                new_folder_parent.Parent_folder_id = New_parent_id
                new_folder_parent.save()
              else:
                new_quiz_parent = Quizz.objects.get(id=Draged_Folder_Id)
                new_quiz_parent.Parent_folder_id = New_parent_id
                new_quiz_parent.save()

        def rename_folder(Folder_Id, Folder_New_Name):
              new_folder_name = Folders.objects.get(id=Folder_Id)
              new_folder_name.Folder_Name = Folder_New_Name
              new_folder_name.save()

        def create_folder(New_Folder_Name, New_Folder_Parent):
            new_folder = Folders(
                Owner_id=request.user.id,
                Folder_Name=New_Folder_Name,
                Parent_folder_id=New_Folder_Parent
            )
            new_folder.save()
            return new_folder.id

        if New_Folder_Name_Post and New_Folder_Parent_Post:
           return JsonResponse({'New_Folder': str(create_folder(New_Folder_Name_Post, New_Folder_Parent_Post))})

        if New_new_Folder_Name_Post and New_new_Folder_Id:
           rename_folder(New_new_Folder_Id,New_new_Folder_Name_Post)

        if New_parent_of_draged_folder_id and Folder_draged_id and File_or_Folder:
           update_folder_parent(Folder_draged_id,New_parent_of_draged_folder_id,File_or_Folder)

        if Folder_To_Delete_ID:
           delete_folder(Folder_To_Delete_ID)

        if New_Quizz_Title and Parent_Quizz_Folder:
          def create_quiz():
              new_quizz = Quizz(
                  Owner_id=request.user.id,
                  Title=New_Quizz_Title,
                  Parent_folder_id=Parent_Quizz_Folder,
                  Settings=['EMPTY']
              )
              new_quizz.save()

              # Create a default question for the new quiz
              default_question = Question(
                  Quizz_id=str(new_quizz.id),
                  Content='Enter your first question ...',
                  Scoring='1',
                  Order='1'
              )
              default_question.save()

              # Encrypt the new quiz ID for the response
              Quizz_id = encrypt_data(str(new_quizz.id))
              return JsonResponse({'URL': str(Quizz_id), 'ID': str(new_quizz.id)})

          if Get_User_Subscription.exists():
              return create_quiz()  # If user has a subscription, create a quiz
          else:
              Quizs_Rowcount = len(Quizs)
              if Quizs_Rowcount < 20:
                  return create_quiz()  # No quizzes, create a new one
              else:
                  print('Upgrade to premium')
                  return JsonResponse({'NONE_URL': 'Upgrade to premium'})

    tree_session_key = encrypt_data(str(request.user.id))

    return render(request, "quizzy/dashboard.html", {
        'Quiz': Quizs,
        'Active': Active,
        'Tree_Key': tree_session_key,
        'Tree_JSON': json.dumps(Tree)
    })

def pricing(request):
  print('going')
  return render(request, "quizzy/pricing.html")

@login_required
def pay(request):
  Subscription = request.GET.get('type')

  User_Subscription = Subscriptions.objects.filter(Owner_id = request.user.id)

  if User_Subscription.exists():
    return redirect('/dashboard')

  if request.method == 'POST':
    New_Subscription_id = request.POST.get('Subscription')
    if New_Subscription_id:
      new_subscription = Subscriptions(
         Owner_id=request.user.id,
         Subscription_type=str(Subscription),
         Subscription_id=New_Subscription_id
      )
      new_subscription.save()
      return JsonResponse({'DATA': 'Success'})

  if int(Subscription) == 1:
    return render(request, "paypal/paypal1.html")
  elif int(Subscription) == 2:
    return render(request, "paypal/paypal2.html")
  elif int(Subscription) == 3:
    return render(request, "paypal/paypal3.html")
  else:
    return redirect('/pricing')


@login_required
def payed(request):
  return render(request, "quizzy/payed.html")


def editor(request):
   Encrypted_Quizz_id = request.GET.get('session')
   try:
    Actual_Quizz_id = decrypt_data(ast.literal_eval(Encrypted_Quizz_id))
   except:
    return redirect('/')
   if Quizz.objects.filter(id = Actual_Quizz_id).exists():
     Quizz_Data = Quizz.objects.get(id = Actual_Quizz_id)
     Quizz_Title = Quizz_Data.Title
     Quizz_Access = Quizz_Data.Settings
     if Quizz_Access[0] == 'EMPTY':
       quizz_access = False
     else:
       quizz_access = True

     #loading the questions
     Get_Quizz_Questions = Question.objects.filter(Quizz_id=Actual_Quizz_id).annotate(order_as_int=Cast('Order', IntegerField())).order_by('order_as_int')
     Quizz_Questions = []
     for User_Quizz_Questions in Get_Quizz_Questions:
       Quizz_Questions.append([User_Quizz_Questions.id, User_Quizz_Questions.Order, User_Quizz_Questions.Content])
    #End loading quetions

     #loading the choices
     Get_Questions_Choices = Choice.objects.filter(Quizz_id=Actual_Quizz_id).order_by('id')
     Questions_Choices = []
     for User_Questions_Choices in Get_Questions_Choices:
       Questions_Choices.append([User_Questions_Choices.id,User_Questions_Choices.Question_id,User_Questions_Choices.Content,User_Questions_Choices.Correction])
     #End loading choices

   else:
      return redirect('/')
   if request.method == 'POST' and Quizz.objects.filter(id = Actual_Quizz_id).exists():

     Updated_Quizz_Title = request.POST.get('Update_Quizz_Title')
     Updated_Question_Content = request.POST.get('Update_Question_Content')
     Question_to_Update_Id = request.POST.get('Question_to_update_Id')
     Question_Order =  request.POST.get('New_Questions_Order')
     New_Question =  request.POST.get('New_Question_Content')
     New_Choice =  request.POST.get('New_Choice')
     New_Choice_Question_Id =  request.POST.get('Question_Id')
     To_Update_Choice_Truth_Value = request.POST.get('Truth_Value')
     To_Update_Choice_Id = request.POST.get('Choice_to_update_id')
     Choice_to_update_Id = request.POST.get('Choice_to_update_Id')
     Updated_Choice_Content = request.POST.get('Updated_Choice_Content')
     Choice_To_Delete_id = request.POST.get('Choice_To_Delete_id')
     Question_To_Delete_Id = request.POST.get('Question_To_Delete_Id')
     Auto_Correct = request.POST.get('Auto_Correct')
     Auto_Correct_2 = request.POST.get('correct2')
     Auto_Correct_3 = request.POST.get('correct3')
     Auto_Correct_4 = request.POST.get('correct4')
     file = request.FILES.get('file')
     Step_1 = request.POST.get('step2')
     Step_2 = request.POST.get('step3')
     Step_3 = request.POST.get('step4')
     Delete_Quizz = request.POST.get('Delete_Quizz')
     Reset_Quizz = request.POST.get('Reset_Quizz')
     Quizz_Password = request.POST.get('Quizz_Password')
     Quizz_unlocked = request.POST.get('Quizz_Unlocked')
     Math_Expressions = request.POST.get('IsMath')
     Latex_2 = request.POST.get('latex2')
     Latex_3 = request.POST.get('latex3')
     Latex_4 = request.POST.get('latex4')



     if Math_Expressions:
       latex_1 = MathExpressions(Actual_Quizz_id)
       return JsonResponse({'DATA': latex_1})

     if Latex_2:
       latex_array_1 = Latex_2
       latex_2 = MathExpressions_2(latex_array_1)
       return JsonResponse({'DATA': latex_2})

     if Latex_4:
       latex_array_2 = Latex_4
       latex_4 = MathExpressions_4(latex_array_2)
       return JsonResponse({'DATA': 'true'})

     if Quizz_unlocked:
       unlock_quizz(Actual_Quizz_id)
       return JsonResponse({'DATA': 'null'})

     if Quizz_Password:
       restrict_quizz(encrypt_data(Quizz_Password),Actual_Quizz_id)
       return JsonResponse({'DATA': 'null'})
     if Reset_Quizz:
       reset_quizz(str(Actual_Quizz_id))
       return JsonResponse({'DATA': 'null'})

     if Delete_Quizz:
      delete_quizz(str(Actual_Quizz_id))
      return JsonResponse({'DATA': 'null'})

     if file:
      convert_to_text = upload_file(file, Actual_Quizz_id)
      request.session['data'] = convert_to_text
      return JsonResponse({'DATA': 'next step'})

     if Step_1:
      session_step_2 = request.session.get('data')
      step_2 = Conversion(session_step_2)
      request.session['data'] = step_2
      return JsonResponse({'DATA': step_2})

     if Step_2:
      session_step_3 = request.session.get('data')
      step_3 = Parser(session_step_3)
      request.session['data'] = step_3
      return JsonResponse({'DATA': step_3})

     if Step_3:
        # Retrieve the session data (default to empty list if not present)
        session_step_4 = request.session.get('data', [])

        # Get the first 20 questions (or less) from session data
        first_20_questions = session_step_4[:20]

        # Remove the first 20 questions from session data
        session_step_4 = session_step_4[20:]

        # Update the session with the remaining questions
        request.session['data'] = session_step_4

        # Ensure session is marked as modified (forces Django to save the session)
        request.session.modified = True

        step_4 = Save_To_DB(first_20_questions, Actual_Quizz_id)

        if not session_step_4:
          return JsonResponse({'DATA': 'true'})
        else:
          return JsonResponse({'DATA': 'next'})

     if Auto_Correct:
       correct_1 = create_exam_array(Actual_Quizz_id)
       return JsonResponse({'DATA': correct_1})

     if Auto_Correct_2:
       correct_2 = process_with_ai(json.loads(Auto_Correct_2))
       return JsonResponse({'DATA': correct_2})

     if Auto_Correct_3:
       correct_3 = parse_correction_into_array(Auto_Correct_3)
       return JsonResponse({'DATA': correct_3})

     if Auto_Correct_4:
       correction_array = json.loads(Auto_Correct_4)
       correct_1 = upload_correction_to_db(correction_array)
       return JsonResponse({'DATA': 'true'})

     if Question_To_Delete_Id:
       delete_question(Question_To_Delete_Id)

     if Choice_To_Delete_id:
       delete_choice(Choice_To_Delete_id)

     if Choice_to_update_Id and Updated_Choice_Content:
       change_choice_content(Choice_to_update_Id, Updated_Choice_Content)

     if To_Update_Choice_Id and To_Update_Choice_Truth_Value:
       change_choice_truth_value(To_Update_Choice_Id,To_Update_Choice_Truth_Value)

     if New_Choice and New_Choice_Question_Id:
       New_Choice_Data = add_choice(New_Choice, New_Choice_Question_Id, Actual_Quizz_id)
       return JsonResponse({'DATA': New_Choice_Data})

     if New_Question:
       New_Question_Data = add_question(New_Question, Actual_Quizz_id)
       return JsonResponse({'DATA': New_Question_Data}) 

     if Question_Order:
       Question_Order_Array = json.loads(Question_Order)
       change_question_order(Question_Order_Array)

     if Updated_Question_Content and Question_to_Update_Id:
       change_question_content(Updated_Question_Content, Question_to_Update_Id)

     if Updated_Quizz_Title:
       change_quizz_title(Updated_Quizz_Title ,Actual_Quizz_id)

   return render(request, "quizzy/editor.html" , {'Quizz_id': str(encrypt_data_2(str(Actual_Quizz_id))),'Quizz_Title': Quizz_Title, 'Quizz_Questions': Quizz_Questions, 'Questions_Choices': Questions_Choices, 'Quizz_Access': quizz_access})

def quiz(request):
   Encrypted_Quizz_id = request.GET.get('session')
   Quizz_Password = request.GET.get('password')
   try:
    Actual_Quizz_id = decrypt_data_2(ast.literal_eval(Encrypted_Quizz_id))
   except:
    return redirect('/')
   if Quizz.objects.filter(id = Actual_Quizz_id).exists():
     Quizz_Data = Quizz.objects.get(id = Actual_Quizz_id)
     Quizz_Title = Quizz_Data.Title
     Quizz_Access = Quizz_Data.Settings
     if Quizz_Access[0] == 'EMPTY':
          quizz_access = True
     else:
          Fetch_Quizz = Quizz.objects.filter(id=Actual_Quizz_id)
          if Quizz_Password and Fetch_Quizz.exists():
              Fetch_Quizz_Key = Quizz.objects.get(id=Actual_Quizz_id)
              if str(decrypt_data(ast.literal_eval(Fetch_Quizz_Key.Settings[1]))) == Quizz_Password:
                quizz_access = True
              else:
                quizz_access = False
          else:
              quizz_access = False

     #loading the questions
     Get_Quizz_Questions = Question.objects.filter(Quizz_id=Actual_Quizz_id).annotate(order_as_int=Cast('Order', IntegerField())).order_by('order_as_int')
     Quizz_Questions = []
     for User_Quizz_Questions in Get_Quizz_Questions:
       Quizz_Questions.append([User_Quizz_Questions.id, User_Quizz_Questions.Order, User_Quizz_Questions.Content])
    #End loading quetions

     #loading the choices
     Get_Questions_Choices = Choice.objects.filter(Quizz_id=Actual_Quizz_id).order_by('id')
     Questions_Choices = []
     for User_Questions_Choices in Get_Questions_Choices:
       Questions_Choices.append([User_Questions_Choices.id,User_Questions_Choices.Question_id,User_Questions_Choices.Content,User_Questions_Choices.Correction])
     #End loading choices

     if request.method == 'POST':
       User_Answers = request.POST.get('User_Answers')

       if User_Answers:
        correct_answers = score(Actual_Quizz_id)

        # Prepare the JSON response with both results and score
        return JsonResponse({'DATA': correct_answers})

   else:
      return redirect('/')
   return render(request,"quizzy/quiz.html", {'Quiz_id':Encrypted_Quizz_id,'Quizz_Title': Quizz_Title ,'Quizz_Questions': Quizz_Questions, 'Questions_Choices':Questions_Choices, 'Quizz_Access': quizz_access})
from django.test import TestCase

# Create your tests here.
def index(request):
    searched = None
    searched_text = request.GET.get("text")
    searched_Author = request.GET.get("Author")
    searched_Author_id = User.objects.filter( username =searched_Author) 
    if searched_Author_id and searched_text : 
        searched = Post.objects.filter(
            Q(post_text__icontains=searched_text) |
            Q(author=searched_Author_id)
            )         
    latest_post_list = Post.objects.order_by('-pub_date')[:5]
    slide = []
    for data in slider.objects.all(): 
        # slide = Post.objects.filter(pk = data) 
        slide.append (list(Post.objects.filter(pk = data.image_id))[0] )
    # slide = Post.objects.filter(pk = 1)
    # output = ', '.join([p.post_text for p in latest_post_list])
    # return HttpResponse(output)
    # template = loader.get_template('weblog/index.html') next code is shortcut
    context = {
        'latest_post_list': latest_post_list,
        'slider' : slide,
        'searched' : searched,
    }
    # return HttpResponse(template.render(context,request)) next code is shortcut
    return  render(request,'weblog/index.html',context)
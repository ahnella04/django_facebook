from django.shortcuts import render, redirect

from facebook.models import Article, Comment

# Create your views here.

def play(request):
    return render(request, 'play.html')


count = 0
def play2(request):
    name = 'ahn ah rim'

    global count
    count = count + 1

    age = 25
    if age > 20:
        status = '성인입니다'
    else:
        status = '청소년입니다'

    diary = ['날씨가 좋았다 - 월', '흐렸다 - 화', '배고팠다 - 수']

    return render(request, 'play2.html', {'name': name, 'cnt': count, 'status': status, 'diary': diary})

def event(request):
    name = '안아림'

    global count
    count = count + 1

    age = 23
    if age > 20:
        year = '성인'
    else:
        year ='청소년'

    if count == 7:
        status = '당첨!'
    else:
        status ='꽝...'

    return render(request, 'event.html', {'name': name, 'cnt': count, 'year': year, 'status': status})

def newsfeed(request):

    #데이터베이스 모든 뉴스피드를 긁어오기
    articles = Article.objects.all()

    return render(request, 'newsfeed.html',{'articles': articles})

def detail_feed(request, pk):

    article = Article.objects.get(pk=pk)

    #코멘트 추가요청이 들어오면 DB에 등록하기
    if request.method == 'POST':
        #코멘트 등록하기
        Comment.objects.create(
            article=article,
            author=request.POST['nickname'],
            text=request.POST['reply'],
            password=request.POST['password']
    )

    return render(request, 'detail_feed.html', {'feed': article })

def new_feed(request):

    # 1)입력한 내용을 받아오기
    if request.method == 'POST':
         # 2) 받아왔으면 그 글을 등록해라
        feed = Article.objects.create(
            author=request.POST['author'],
            title=request.POST['title'],
            text=request.POST['content']+'-추신: 감사합니다',
            password=request.POST['password']
        )

        return redirect(f'/feed/{feed.pk}')
    return render(request, 'new_feed.html')

def edit_feed(request, pk):
    # 1)수정할 글의 정보를 불러오기
    feed = Article.objects.get(pk=pk)

    if request.method == 'POST':
        # 2) 받은 정보로 수정해주세요
        feed.title = request.POST['title']
        feed.author = request.POST['author']
        feed.author = request.POST['content']
        feed.save()

        return redirect(f'/feed/{feed.pk}/')
    #return redirect('/feed/'+ feed.pk)

    return render(request, 'edit_feed.html', { 'feed': feed })

def remove_feed(request, pk):
    feed = Article.objects.get(pk=pk)

    if request.method=='POST':
        #비밀번호 확인하기
        if request.POST['pw'] == feed.password:
            # 그 글을 삭제해주세요
            feed.delete()
            return redirect('/')
        else:
            print('비밀번호가 틀렸습니다')

    return render(request, 'remove_feed.html')
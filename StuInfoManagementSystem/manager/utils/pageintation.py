"""
自定义的分页组件
"""

from django.utils.safestring import mark_safe

class Pageination(object):
    def __init__(self, request, queryset, page_size=10, page_param="page", plus=5):
        """_summary_

        Args:
            request (_type_): _description_
            queryset (_type_): _description_
            page_size (int, optional): _description_. Defaults to 10.
            page_param (str, optional): _description_. Defaults to "page".
            plus (int, optional): _description_. Defaults to 5.
        """
        
        import copy
        query_dict = copy.deepcopy(request.GET)
        query_dict._mutable = True
        self.query_dict = query_dict
        
        page = request.GET.get(page_param,"1")
        if page.isdecimal():
            page = int(page)
        else:
            page = 1

        self.page = page
        self.page_size = page_size
        
        self.start = (page - 1) * page_size
        self.end = page * page_size
        
        self.page_queryset =  queryset[self.start:self.end]
        
        total_count = queryset.count()
        total_page_count, div = divmod(total_count, page_size)
        self.total_page_count = total_page_count
        if div:
            self.total_page_count += 1
        else:
            self.total_page_count = total_page_count
        
        self.page_param = page_param
        self.plus = plus
        
    def html(self):
        if self.total_page_count <= 2 * self.plus + 1:
            start_page = 1
            end_page = self.total_page_count
        elif self.page <= self.plus:
            start_page = 1
            end_page = 2 * self.plus + 1
        elif (self.page + self.plus) > self.total_page_count:
            start_page = self.total_page_count - 2 * self.plus
            end_page = self.total_page_count
        else:
            start_page = self.page - self.plus
            end_page = self.page + self.plus
    
        page_str_list = []
        
        self.query_dict.setlist(self.page_param,[1])
        page_str_list.append('<li><a href="?{}" >首页</a></li>'.format(self.query_dict.urlencode()))
        # 上一页
        if self.page > 1:
            self.query_dict.setlist(self.page_param,[self.page - 1])
            prev = '<li><a href="?{}" >上一页</a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param,[1])
            prev = '<li><a href="?{}" >上一页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(prev)
        # 页面
        for i in range(start_page,end_page + 1):
            self.query_dict.setlist(self.page_param,[i])
            if i == self.page:
                ele = '<li class="active" ><a href="?{}" >{}</a></li>'.format(self.query_dict.urlencode(),i)
            else:
                ele = '<li ><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(),i)
            page_str_list.append(ele)
        # 下一页
        if self.page < self.total_page_count:
            self.query_dict.setlist(self.page_param,[self.page + 1])
            prev = '<li><a href="?{}" >下一页</a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param,[self.total_page_count])
            prev = '<li ><a href="?{}" >下一页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(prev)
        # 尾页
        self.query_dict.setlist(self.page_param,[self.total_page_count])
        page_str_list.append('<li ><a href="?{}" >尾页</a></li>'.format(self.query_dict.urlencode()))

        search_string = """
            <li>
                <form style="float:left;margin-left:-1px;" method="get" >
                    <input name="page" style="position:relative;float:left;display:inline-block;width: 80px;border-radius: 0;" type="text" class="form-control" placeholder="页码" >
                    <button style="border-radius: 0;" class="btn btn-default" type="submit" >跳转</button>
                </form>
            </li>
        """
        page_str_list.append(search_string)
        page_string = mark_safe("".join(page_str_list))
        return page_string
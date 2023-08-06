import os
import io
from django.http.response import HttpResponse
from django.shortcuts import render as django_render
import Mujocso
from bs4 import BeautifulSoup

javascript_files = html_files = css_files = font_files = []

mujocso_location = Mujocso.__file__
mujocso_location = mujocso_location.replace("\\","/")
mujocso_location = mujocso_location.split("/")
mujocso_location.pop()
mujocso_location = '/'.join(mujocso_location)

allowed_font_formats = ['ttf', 'otf', 'eot', 'woff2', 'woff']

for root, directory, files in os.walk(mujocso_location+'/template_files'):
    for file in files:
        if(file.endswith('.js')):
            javascript_files.append(file)

        elif(file.endswith('.html')):
            html_files.append(file)

        elif(file.endswith('.css')):
            css_files.append(file)

        for font_name in allowed_font_formats:
            if(file.endswith('.'+str(font_name))):
                font_files.append(file)
        
        else:
            continue

class MujocsoException(Exception):
    pass

class Mujocso:
    def render(headers=None, page_title='Mujocso Page', style=[], template=None):
        global mujocso_location

        allowed_header_inputs = ['value', 'size']
        avaliable_styles = ['CBRORANGE', 'CENTERTITLEORANGE']
        avaliable_page_styles = []
        avaliable_templates = ['CBRO404']
        page_body = ''
        page_style = ''

        if(template != None):
            if(type(template) == str):
                if(template.upper() in avaliable_templates):
                    with io.open(file=mujocso_location+'/template_files/'+str(template).upper()+'.css', encoding='UTF-8') as template_css:
                        template_css = template_css.read()
                    page_style = template_css
                else:
                    raise MujocsoException('Template not found')
            else:
                raise MujocsoException('Template type is not valid')

        if(style != [] and template == None and type(style) == list):
            for s in style:
                if(s in avaliable_page_styles):
                    with io.open(file=mujocso_location+'/template_files/'+str(s).upper()+'.css', encoding='UTF-8') as style_css:
                        style_css = style_css.read()
                        style_css = style_css.replace('*{ /* Mujocso Css Format Start */\n', '')
                        style_css = style_css.replace('\n} /* Mujocso Css Format End */', '')
                        page_style += style_css
                else:
                    if(s.endswith(";") == False):
                        page_style += s+';'
                    else:
                        page_style += s
                    

        if(headers != None):
            if(type(headers) == list):
                for header in headers:
                    if(type(header) == dict):
                        for key in allowed_header_inputs:
                            if(key in header and int(header['size']) <= 6):
                                continue
                            else:
                                raise MujocsoException('Header values must be valid')
                    else:
                        raise MujocsoException('Header values must be a dictionary')
            else:
                raise MujocsoException('The headers must be a list')

        
        with io.open(file=mujocso_location+'/template_files/page.html', encoding='UTF-8') as page:
            o = page.read()

        o = o.replace(
            '{*PAGE_TITLE*}',
            page_title 
            )
        
        if(headers != None and type(headers) == list):
            for header in headers:
                styleable = 'style' in header
                header_tag = 'h'+str(header['size'])
                styles_temp = ''
                if(styleable):
                    if(type(header['style']) == list):
                        for style in header['style']:
                            if(style.upper() in avaliable_styles):
                                with io.open(file=mujocso_location+'/template_files/'+str(style).upper()+'.css', encoding='UTF-8') as style_css:
                                    style_css = style_css.read()
                                    style_css = style_css.replace('*{ /* Mujocso Css Format Start */\n', '')
                                    style_css = style_css.replace('\n} /* Mujocso Css Format End */', '')
                                    styles_temp += style_css
                            else:
                                if(style.endswith(";") == False):
                                    styles_temp += '\n'+style+';'
                                else:
                                    styles_temp += '\n'+style
                        
                    elif(type(header['style']) == str):
                        if(header['style'].upper() in avaliable_styles):
                            with io.open(file=mujocso_location+'/template_files/'+str(header['style']).upper()+'.css', encoding='UTF-8') as style_css:
                                style_css = style_css.read()
                                style_css = style_css.replace('*{ /* Mujocso Css Format Start */\n', '')
                                style_css = style_css.replace('\n} /* Mujocso Css Format End */', '')
                                styles_temp += style_css
                        else:
                            if(header['style'].endswith(";") == False):
                                styles_temp += header['style']+';'
                            else:
                                styles_temp += header['style']
                    else:
                        raise MujocsoException("The headers style type must be string or list")

                    styles_temp = styles_temp.replace('\n', ' ').replace('  ', ' ')
                    style_param = 'style="'+styles_temp+'"'
                    add_to_body = '<'+header_tag+' '+style_param+'>'+str(header['value'])+'</'+header_tag+'>'
                else:
                    add_to_body = '<'+header_tag+'>'+str(header['value'])+'</'+header_tag+'>'
                
                page_body += add_to_body
                page_body += '\n' 
        

        o = o.replace(
            '{*BODY_SPACE*}',
            '<body>\n'+
            page_body+
            '\n</body>'
            )

            

        if(page_style != ''):
            
            o = o.replace(
                '{*STYLE_SPACE*}',
                '<style>\n'+
                page_style+
                '\n</style>'
                )
        else:
            o = o.replace(
                '{*STYLE_SPACE*}',
                ''
                )

        soup = BeautifulSoup(o, 'html.parser')
        output = soup.prettify()
        return HttpResponse(output)
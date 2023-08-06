import discord


'''
author, field, footerの指定方法が特殊なので書き方の例を残しておきます。


~ author ~

author={
    'name': 'author name',
    'url': 'author url',
    'icon_url': 'author icon url'
}

もしくは、

author=author_dict(
    name = 'author name',
    url = 'author url',
    icon_url = 'author icon url'
)


~ field ~

指定するフィールドが一つだけの場合でもリスト型にしてください。

fields=[
{
    'name': 'field name',
    'value': 'field value',
    'inline': bool
},
{
    'name': 'field name',
    'value': 'field value',
    'inline': bool
}
]

もしくは、

fields=[
field_dict(
    name = 'field name',
    value = 'field value',
    inline = bool
),
field_dict(
    name = 'field name',
    value = 'field value',
    inline = bool
)
]

~ footer ~

footer={
    'text': 'footer text',
    'icon_url': 'footer icon url'
}

もしくは、

footer=footer_dict(
    text = 'footer text',
    icon_url = 'footer icon url'
)
'''


# 送信者の設定をする際のdictを分かりやすく定義するための関数
# 返り値：dict
def author_dict(*, name: str = None, url: str = None, icon_url: str = None):
    # author_dict(name='author name', url='author url', icon_url='author icon url')
    return_dict = {}
    if name is not None:
        return_dict['name'] = name
    if url is not None:
        return_dict['url'] = url
    if icon_url is not None:
        return_dict['icon_url'] = icon_url
    return return_dict


# フィールドの設定をする際のdictを分かりやすく定義するための関数
# 返り値：dict
def field_dict(*, name: str = None, value: str = None, inline: bool = True):
    # field_dict(name='field name', value='field value', inline=bool)
    return_dict = {}
    if name is not None:
        return_dict['name'] = name
    if value is not None:
        return_dict['value'] = value
    if inline is not True:
        return_dict['inline'] = inline
    return return_dict


# フッターの設定をする際のdictを分かりやすく定義するための関数
# 返り値：dict
def footer_dict(*, text: str = '', icon_url: str = ''):
    # footer_dict(text='footer text', icon_url='footer icon url')
    return_dict = {}
    if text != '':
        return_dict['text'] = text
    if icon_url != '':
        return_dict['icon_url'] = icon_url
    return return_dict


# Embedを作成
# 返り値：discord.Embed
def make(*, title: str = None, description: str = None, url: str = None, color: int = None, footer: dict = None, image: str = None, thumbnail: str = None, author: dict = None, fields: list = None):
    embed = discord.Embed()
    if title is not None:
        # make(title='title')
        embed.title = title
    if description is not None:
        # make(description='description')
        embed.description = description
    if url is not None:
        # make(url='url')
        embed.url = url
    if color is not None:
        # make(color=colour)
        embed.colour = color
    if footer is not None:
        # make(footer={'text': 'text', 'icon_url': 'icon url'})
        # make(footer_dict(text='text', icon_url='icon url'))
        if 'text' in footer.keys() and 'icon_url' in footer.keys():
            embed.set_footer(text=footer['text'], icon_url=footer['icon_url'])
        if 'text' not in footer.keys() and 'icon_url' in footer.keys():
            embed.set_footer(icon_url=footer['icon_url'])
        if 'text' in footer.keys() and 'icon_url' not in footer.keys():
            embed.set_footer(text=footer['text'])
    if image is not None:
        # make(image='iamge url')
        embed.set_image(url=image)
    if thumbnail is not None:
        # make(thumbnail='image url')
        embed.set_thumbnail(url=thumbnail)
    if author is not None:
        # make(author={'name': 'author name', 'url': 'author url', 'icon_url': 'author icon url'})
        # make(author_dict(name='author name', url='author url', icon_url='author icon url'))
        author_name = ''
        author_url = ''
        author_icon_url = ''
        if 'name' in author.keys():
            author_name = author['name']
        if 'url' in author.keys():
            author_url = author['url']
        if 'icon_url' in author.keys():
            author_icon_url = author['icon_url']
        embed.set_author(name=author_name, url=author_url, icon_url=author_icon_url)
    if fields is not None:
        # make(fields=[{'name': 'field name', 'value': 'field value', 'inline': bool}, {'name': 'field name', 'value': 'field value', 'inline': bool}])
        # make([field_dict(name='field name', value='field value', inline=bool), field_dict(name='field name', value='field value', inline=bool)])
        for f in fields:
            field_name = None
            field_value = None
            field_inline = True
            if 'name' in f.keys():
                field_name = f['name']
            if 'value' in f.keys():
                field_value = f['value']
            if 'inline' in f.keys():
                field_inline = f['inline']
            embed.add_field(name=field_name, value=field_value, inline=field_inline)
    return embed


# Embedを編集
# discord.Embed.edit()
def edit(self, *, title: str = None, description: str = None, url: str = None, color: int = None, footer: dict = None, image: str = None, thumbnail: str = None, author: dict = None):
    if title is not None:
        # discord.Embed.edit(title='title')
        self.title = title
    if description is not None:
        # discord.Embed.edit(description='description')
        self.description = description
    if url is not None:
        # discord.Embed.edit(url='url')
        self.url = url
    if color is not None:
        # discord.Embed.edit(color=colour)
        self.colour = color
    if footer is not None:
        # discord.Embed.edit(footer={'text': 'footer text', 'icon_url': 'footer icon url'})
        # discord.Embed.edit(footer=footer_dict(text='footer text', icon_url='footer icon url'))
        footer_text = self.footer.text
        footer_icon_url = self.footer.icon_url
        if 'text' in footer.keys():
            footer_text = footer['text']
        if 'icon_url' in footer.keys():
            footer_icon_url = footer['icon_url']
        self.set_footer(text=footer_text, icon_url=footer_icon_url)
    if image is not None:
        # discord.Embed.edit(image='image url')
        self.set_image(url=image)
    if thumbnail is not None:
        # discord.Embed.edit(thumbnail='thumbnail url')
        self.set_thumbnail(url=thumbnail)
    if author is not None:
        # discord.Embed.edit(author={'name': 'author name', 'icon_url': 'author icon url', 'name': 'author name'})
        author_url = self.author.url
        author_icon_url = self.author.icon_url
        author_name = self.author.name
        if 'url' in author.keys():
            author_url = author['url']
        if 'icon_url' in author.keys():
            author_icon_url = author['icon_url']
        if 'name' in author.keys():
            author_name = author['name']
        self.set_author(url=author_url, icon_url=author_icon_url, name=author_name)


# フィールドを一度に複数追加
# discord.Embed.multiple_add_fields()
def multiple_add_fields(self, fields: list):
    # discord.Embed.multiple_add_fields([{'name': 'field name', 'value': 'field value', 'inline': bool}, {'name': 'field name', 'value': 'field value', 'inline': bool}])
    # discord.Embed.multiple_add_fields([field_dict(name='field name', value='field value', inline=bool), field_dict(name='field name', value='field value', inline=bool)])
    for f in fields:
        field_name = None
        field_value = None
        field_inline = True
        if 'name' in f.keys():
            field_name = f['name']
        if 'value' in f.keys():
            field_value = f['value']
        if 'inline' in f.keys():
            field_inline = f['inline']
        self.add_field(name=field_name, value=field_value, inline=field_inline)


# フィールドを一度に複数削除
# discord.Embed.multiple_remove_fields()
def multiple_remove_fields(self, index: list):
    # discord.Embed.multiple_remove_fields([1, 2, 3...])
    index = sorted(index, reverse=True)
    for i in index:
        self.remove_field(i)


discord.Embed.multiple_add_fields = multiple_add_fields
discord.Embed.multiple_remove_fields = multiple_remove_fields

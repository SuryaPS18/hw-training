from parsel import Selector
html_text = """
<html>
<head>
    <title>Example Page</title>
</head>
<body>
    <div class="content">
        <h1>Hello, World!</h1>
        <p>This is a paragraph.</p>
    </div>
    <ul>
        <li>Item 1</li>
        <li>Item 2</li>
        <li>Item 3</li>
    </ul>
    <div class="image">
    <img src="example.jpg">
    <img src="picture.jpg" >
    </div>
    <div>
        <a href="/page1.html">Link 1</a>
        <a href="/page2.html">Link 2</a>
        <a href="https://example.com">Link 3</a>
        <a href="/page3.html">Link 4</a>
    </div>

    
    <ul class="_033281ab" style="columns:2" aria-label="Property details">
        <li>
            <span class="_3af7fa95">Type</span>
            <span class="_812aa185">Townhouse</span>
        </li>
        <li>
            <span class="_3af7fa95">Purpose</span>    
            <span class="_812aa185">For Rent</span>
        </li>
        <li>
            <span class="_3af7fa95">Reference no.</span>
            <span class="_812aa185" >Bayut - 102164-g69R6d</span>
        </li>
    </ul>
    
    <div>
        <a id="abc_123" name="bismi" age="20">data 1</a>
        <a id="xyz" name="sree" age="30">data 2</a>
        <a id="abc_456" name="surya" age="36">data 3</a>
        <a id="def" name="arya" age="40">data 4</a>
        <a id="qwe" name="ammu" > data 5 </a>
    </div>

    <table>
    <tr>
        <th>Product</th>
        <td>product 1</td>
        <td>product 2</td>
        <td>product 3</td>
    </tr>
    <tr>
        <th>Price</th>
        <td>10</td>
        <td>20</td>
        <td>30</td>
    </tr>
</table>
</body>
</html>
"""

# Create a Selector object
selector = Selector(text=html_text)
title=selector.xpath('//title/text()').get()
h1=selector.xpath('//div[@class="content"]//h1/text()').get()
p=selector.xpath('//div[@class="content"]//p/text()').get()
li =selector.xpath('(//li)[2]/text()').get()
img=selector.xpath('//div[@class="image"]//img/@src').get()
img1=selector.xpath('//div[@class="image"]//img[2]/@src').get()
# type=selector.xpath('//*[contains(@class,"_033281ab")]//*[@aria-label="Purpose"]/text()').get()
# type=selector.xpath('//*[contains(@class,"_033281ab")]/li[2]/span[2]/text()').get()
type1=selector.xpath('//ul/li[2]/span[2]/text()').get()
type2=selector.xpath('//span[@aria-label="Purpose"]/text()').get()
purpose=selector.xpath('//ul[2]//li[2]/span[2]/text()').get()
purpose1=selector.xpath("//span[@class='_3af7fa95' and text()='Type']/following-sibling::span[@class='_812aa185']/text()").get()

type3=selector.xpath("//span[text()='For Rent']/text()").get()  #full match
type4=selector.xpath("//span[contains(text(),'For Rent')]/text()").get()
type5=selector.xpath("//span[contains(.,'For Rent')]/text()").get()
type6=selector.xpath('//li[span/text()="Purpose"]/preceding-sibling::li/span[2]/text()').get() 

type7=selector.xpath("//ul//descendant::span[2]/text()").get()
# type7=selector.xpath("//ul//descendant::/text()").get()
link = selector.xpath("//a[starts-with(@href, '/')]/@href").getall() 
link1 = selector.xpath("////a[contains(@href, '://')]/@href").get()
#comparison and operator

data=selector.xpath('//a[@id != "xyz"]/text()').getall()
data1=selector.xpath('//a[@age> 25]/text()').getall()
data2=selector.xpath('//a[@name and @age]/text()').getall()
# data2=selector.xpath('//a[starts-with(@id,"abc") and position()=3]/text()').get()
data3=selector.xpath("//a[@name or @age]/text()").getall()
union=selector.xpath("//span[.='Purpose' or .='For Rent']/text()").getall()

# axes method
self=selector.xpath("//th[1]//self::th/text()").get()
child=selector.xpath("//tr[2]//child::td/text()").get()
descendant=selector.xpath("//table//descendant::th/text()").getall()
following=selector.xpath("//li//following::span/text()").getall()
following_sib=selector.xpath("//span[.='Reference no.']//following-sibling::span/text()").get()
preceding=selector.xpath("//span[.='Reference no.']/preceding::span/text()").getall()
preceding_sib=selector.xpath("//span[.='Townhouse']/preceding-sibling::span/text()").getall()





# test=selector.xpath('//div/*')


# print(title)
# print(h1)
# print(p)
# print(li)
# print(img)
# print(img1)
# print(test)
# print(type2)
# print(purpose2)
# print(type3)
# print(type4)
# print(type5)
# print(type6)
# print(link)
# print(link1)
# print(data)
# print(data1)
# print(data2)
# print(data3)
# print(union)
# print(self)
# print(child)
# print(descendant)
# print(following)
# print(following_sib)
# print(preceding)
# print(preceding_sib)



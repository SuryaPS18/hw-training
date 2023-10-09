# xpath basic format

# xpath =//tagname[@Attribute='Value']

# common rules

# / --> select child node from parent node
# // --> select node anywhere on html dom
#  = --> fully match
#  , --> partial match
#  * --> to match any element
#  . --> string
#  text() --> full text match
#  contain(text()) --> partial text match
#  collection -->()[]
#  start-with
#  end-with
#  position

# comparison:-
#         =
#         !=
#         >
#         and
#         or

#  union --> | (join results)

#  xpath axes methods

# parent --> //tagname[@Attribute='Value']//parent::tagname
# child --> //tagname[@Attribute='Value']//child::tagname
# self --> //tagname[@Attribute='Value']//self::tagname   (current tag )
# descendant -->//tagname[@Attribute='Value']//descendant::tagname  (select children,grandchildren of cuurent tag)
#  descendant-or-self -->//tagname[@Attribute='Value']//descendant-or-self::tagname   (select current tag and all descendant)
# following --> //tagname[@Attribute='Value']//following::tagname            (select all tag that appear after the current tag)
#  following-sibling -->//tagname[@Attribute='Value']//following-sibling::tagname    (select all tag that have same parent)
#  preceding --> select all tag that appear before the current tag
#  preceding-sibling --> select all the tag that have same parent as current tag anf appear before the current tag

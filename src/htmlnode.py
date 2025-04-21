class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        prop_html = ""
        for attri in self.props:
            prop_html += " " + attri + "=" + f'"{self.props[attri]}"'
        return prop_html

    def __repr__(self):
        return f"TextNode(tag: {self.tag}, value: {self.value}, children: {self.children}, props:{self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)
        
    def to_html(self):
        if self.value == None:
            raise ValueError("LeafNode requires a non-None value.")
        elif self.tag == None:
            return self.value
        elif self.props == None:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        else:
            prop_html = self.props_to_html()
            return f"<{self.tag}{prop_html}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("ParentNode requires a non-None tag")
        elif self.children == None:
            raise ValueError("ParentNode requires non-None children")
        inner_html = ""
        for node in self.children:
            inner_html += node.to_html()
        if self.props != None:             
            return f"<{self.tag}{self.props_to_html()}>{inner_html}</{self.tag}>"
        else:
            return f"<{self.tag}>{inner_html}</{self.tag}>"
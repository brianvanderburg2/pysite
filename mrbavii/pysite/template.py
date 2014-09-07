"""
A simple template mechanism.

This class compiles a template file into a python code object
and then executes the code object with a variables dictionary
"""

import codecs

from .error import Error

class TemplateError(Error):
    pass

class _TemplateCompiler(object):
    """ This class translates a template into a python code object """

    def reset(self):
        """ Reset internals to an empty state """
        self._code = ""
        self._indent = 0
        self._line = 0

    def indent(self):
        """ Increase the indent counter """
        self._indent += 1

    def dedent(self):
        """ Decrease the indent counter """
        self._indent -= 1

    def code(self, s):
        """ Write code, properly indented """
        self._code += ('    ' * self._indent) + s + '\n'

    def handle_text(self, text):
        """ Create code to emit plain text """
        self.code("self.write(" + repr(text) + ")")

    def handle_if(self, contents):
        """ Create code for the if section """
        parts = contents.split('|')
        if len(parts) == 0:
            raise TemplateError("No if condition")

        var = parts.pop(0).strip()
        name = "var_" + str(self._indent)

        self.build_var(name, var)
        self.build_modifiers(name, parts)
        self.code("if " + name + ":")
        self.indent()
    
    def handle_else(self):
        self.dedent()
        self.code("else:")
        self.indent()

    def handle_endif(self):
        self.dedent()
        var = "var_" + str(self._indent)
        self.code("del " + var)

    def handle_for(self, contents):
        parts = contents.split()
        var = "var_" + str(self._indent)
        name = parts.pop(0).strip()
        iterable = parts.pop(0).strip()
        self.build_var(var, iterable)
        self.code(var + "_idx = 0")
        self.code("for " + var + "_iter in " + var + ":")
        self.indent()
        self.code("self.vars['" + name + "'] = " + var + "_iter")
        self.code("self.vars['" + name + "_idx'] = " + var + "_idx")

    def handle_endfor(self):
        var = "var_" + str(self._indent - 1)
        self.code(var + "_idx += 1")
        self.dedent()
        self.code("del " + var)
        self.code("del " + var + "_iter")
        self.code("del " + var + "_idx")

    def handle_block(self, content):
        name = content.strip()
        self.code("self.start_block('" + name + "')")
    
    def handle_endblock(self):
        self.code("self.finish_block()")

    def handle_call(self, contents):
        parts = contents.split(',')
        var = "var_" + str(self._indent)    
        name = parts.pop(0).strip()

        self.code(var + " = {}")
        for param in parts:
            (pname, pvalue) = param.split('=')
            self.build_var(var + "['" + pname.strip() + "']", pvalue)
            
        self.code("self.call('" + name + "', " + var + ")")
        self.code("del " + var)
    

    def handle_var(self, contents):
        parts = contents.split('|')
        var = parts.pop(0).strip()

        self.build_var("output", var)
        self.build_modifiers("output", parts)
        self.code("self.write(output)")
        self.code("del output")

    def handle_action(self, contents):
        words = contents.split(None, 1)

        if len(words):
            action = words.pop(0).strip()
        else:
            # TODO: error
            action=""

        if len(words):
            remainder = words.pop(0)
        else:
            remainder = ""

        if action == "if":
            self.handle_if(remainder)
            return
        
        if action == "else":
            self.handle_else()
            return

        if action in "endif":
            self.handle_endif()
            return

        if action == "for":
            self.handle_for(remainder)
            return

        if action == "endfor":
            self.handle_endfor()
            return

        if action == "block":
            self.handle_block(remainder)
            return

        if action == "endblock":
            self.handle_endblock()
            return

        if action == "call":
            self.handle_call(remainder)
            return

    def handle_section(self, contents):
        """ Handle a generic block """
        contents = contents.strip()

        # Check empty block
        if len(contents) == 0:
            return

        # Check comment
        if contents[0] == '#':
            return

        # Check for variable emission
        if contents[0] == '$':
            self.handle_var(contents[1:])
            return

        # Check for action
        if contents[0] == '%':
            self.handle_action(contents[1:])
            return

        # Check for literal
        if contents[0] == '{':
            self.handle_text("{");
            return

        if contents[0] == '}':
            self.handle_text("}")
            return

    def build_var(self, var, tvar):
        """ Build a variable and it's modifiers """
        # self.check(tvar)

        p = tvar.find('.')
        if p >= 0:
            # We found an outer section
            name = tvar[:p]
            remainder = tvar[p:]
        else:
            # We didn't find an outer section
            name = tvar
            remainder = ''

        self.code(var + " = self.vars['" + name + "']" + remainder)

    def build_modifiers(self, var, mods):
        for m in mods:
            self.code(var + " = self.modify('" + m.strip() + "'," + var + ")")
        pass

    def compile_line(self, contents):
        """ Compile the line """
        start = 0
        pos = contents.find('{', start)
        while pos >= 0:
            # Everything up to
            self.handle_text(contents[start:pos])

            # Handle the contents
            end = contents.find('}', pos + 1)
            if(end >= 0):
                self.handle_section(contents[pos + 1:end])
                start = end + 1
            else:
                # TODO: error
                print("Uh oh\n");
                start = pos + 1

            # Find next
            pos = contents.find('{', start)

        # The end
        self.handle_text(contents[start:])

    def compile(self, filename):
        """ Compile the entire contents """
        self.reset()
        with codecs.open(filename, "rU" "UTF-8") as handle:
            self.filename = filename
            line = handle.readline()
            
            while len(line):
                self._line += 1
                self.compile_line(line)
                line = handle.readline()

        # The results
        print(self._code)




if __name__ == "__main__":
    t = _TemplateCompiler()
    t.compile("template.test")
        


        
        
        

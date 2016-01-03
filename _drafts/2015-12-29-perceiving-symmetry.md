---
layout: post
title: "Understanding Variational Inference"
comments: true
categories: blog
tags:
- bayes
- statistics
- machine-learning
- data-science

---

    def resolve_address(self, segment, index):
        self.write('@' + str(segment))
        if segment == 'pointer':
            self.write('D=A')
        else:
            self.write('D=M')
        self.write('@' + str(index))
        self.write('A=D+A') # D is segment

VS


        if segment == 'pointer'
            self.write('@' + str(segment))
            self.write('D=A')
            self.write('@' + str(index))
            self.write('A=D+A') # D is segment
        else:
            self.write('@' + str(segment))
            self.write('D=M')
            self.write('@' + str(index))
            self.write('A=D+A') # D is segment


##

    def resolve_address(self, segment, index):
        address = self.addresses.get(segment)
        if segment in ['pointer', 'temp', 'static']:
            self.write('@R' + str(address + index))
        elif segment in ['local', 'argument', 'this', 'that']:
            self.write('@' + address)
            self.write('D=M')
            self.write('@' + str(index))
            self.write('A=D+A') # D is segment base
        else:
            self.raise_unknown(segment)

VS

    def resolve_address(self, segment, index):
        if segment in ['pointer', 'temp', 'static']:
            if segment == 'pointer':
                self.write('@R' + str(3 + index))
            elif segment == 'temp':
                self.write('@R' + str(5 + index))
            elif segment == 'static':
                self.write('@R' + str(16 + index))
        elif segment in ['local', 'argument', 'this', 'that']:
            self.write('@' + self.addresses.get(segment))
            self.write('D=M')
            self.write('@' + str(index))
            self.write('A=D+A') # D is segment
        else:
            self.raise_unknown(segment)

    def address_dict(self):
        return {
            'local': 'LCL', # Base R1
            'argument': 'ARG', # Base R2
            'this': 'THIS', # Base R3
            'that': 'THAT', # Base R4
            'pointer': 3, # Edit R3, R4
            'temp': 5, # Edit R5-12
            'static': 16, # Edit R16 - R255
        }

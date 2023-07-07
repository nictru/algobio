#!/usr/bin/env python3

from needleman_wunsch import NeedlemanWunsch, main

class Hirschberg(NeedlemanWunsch):
    def __align__(self, s: str, t: str):
        delim = len(s)//2

        s1 = s[:delim]
        t1 = t
        D1, B1 = super().__generate_matrix__(s1, t1)

        s2 = s[delim:][::-1]
        t2 = t[::-1]
        D2, B2 = super().__generate_matrix__(s2, t2)

        summarized = D1[-1] + D2[-1][::-1]
        min_index = summarized.argmin()
        
        if len(s1) == 1:
            end_index = min_index+1
            alignment1 = self.__backtracking__(B1[:,:end_index], s1, t1[:end_index])
        else:
            alignment1 = self.__align__(s[:delim], t[:min_index])

        if len(s2) == 1:
            end_index = len(t2)-min_index+1
            alignment2 = self.__backtracking__(B2[:,:end_index], s2, t2[:end_index])
        else:
            alignment2 = self.__align__(s[delim:], t[min_index:])

        alignment = alignment1[0] + alignment2[0], alignment1[1] + alignment2[1]

        return alignment
    
    def __str__(self):
        return self.alignment[0] + "\n" + self.alignment[1]


if __name__ == '__main__':
    main("Hirschberg algorithm", Hirschberg)

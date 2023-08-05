#!/usr/bin/env python3

from shelltable import Table

if __name__ == '__main__':
    a = Table()
    a.add_column('ID', size=5)
    a.add_column('Author', size=22)
    a.add_column('Title', size=-1)
    a.add_row('001', 'Stephen Hawking', 'Dal Big Bang ai Buchi Neri')
    a.add_row('203', 'Luciano De Crescenzo', 'Così Parlò Bellavista')
    a.add_row('X', 'test', 'Perspiciatis et aliquam dolor eaque. Vel vel nobis adipisci dignissimos vero quo repellendus. Quia a praesentium magni. Placeat omnis dolorem ut in sed ut voluptate.')
    print(a)

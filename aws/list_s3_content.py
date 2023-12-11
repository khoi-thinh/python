from tkinter import *
window=Tk()

import boto3
s3 = boto3.resource('s3')


def list_s3_bucket():
    for bucket in s3.buckets.all():
        t1.insert(END,bucket.name)
        t1.insert(END,"\n")

def list_s3_content():
    #bucket_name = e2_value.get()
    bucket_name = t1.get(ANCHOR)
    my_bucket = s3.Bucket(bucket_name)
    for file in my_bucket.objects.all():
        try:
            #t2.delete(1.0, END)
            t2.delete(0, END)
            t2.insert(END,file.key)
            t2.insert(END,"\n")
        except s3.meta.client.exceptions.NoSuchBucket:
            t2.insert(END,"Error")


b1 = Button(window, text="List Buckets", command=list_s3_bucket)
b1.grid(row=0,column=0)

b2 = Button(window, text="List Bucket Content", command=list_s3_content)
b2.grid(row=0,column=1)


'''
e1_value=StringVar()
e1=Entry(window,textvariable=e1_value)
e1.grid(row=0,column=1)
'''

#e2_value=StringVar()
#e2=Entry(window,textvariable=e2_value)
#e2.grid(row=0,column=2)

t1=Listbox(window,height=50,width=50)
t1.grid(row=1,column=0)

t2=Listbox(window,height=50,width=50)
t2.grid(row=1,column=1)


window.mainloop()

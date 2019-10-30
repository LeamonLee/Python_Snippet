import subprocess
import six
output = subprocess.Popen('xrandr | grep "\*" | cut -d" " -f4',shell=True, stdout=subprocess.PIPE).communicate()[0]
print(output)

if isinstance(output, six.string_types):
    print(output.split(' '))
elif isinstance(output, bytes):
    output = output.decode("utf-8").split('\n')
    print(output)
    print(type(output))
    for pos in output:
        if 'x' in pos:
            lstPos = pos.split('x')
            print("lstPos: ", lstPos)
        else:
            print("x is not in the list")
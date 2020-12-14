# Python_Y86-64

Tammas Hicks
Y86-64 Simulator
Nov 2020

This was inspired by the Y86-64 simulator we used in CIS 314.
Credit goes to github user Boginw for the original simulator,
written in JS, HTML, and CSS. At the time I was making this
we were in the middle of the pandemic, and students were all
learning from home. I was reading frequently of poor students
with bad internet connection having trouble with access to
school materials. I decided I wanted to build a desktop
version of the Y86-64 simulator so that students with poor
internet access would still have access to relevant learning
materials.

As time goes on I'm going to keep releasing features for this.
Ideally this will include a 'compiler' which can compile
written python into Y86-64 assembly code.


PARTS OF THE PROCESSOR

Processor:
  This is the main body of the processor. It's sole job is
  the arrangement of the processor, as well as its component
  pieces. I highly recommend importing just the processor file
  into another file and doing unitests there with a newly
  instantiated Processor object. as it stands, the state and
  error libraries are incomplete. I still need to update 
  them so that they contain more possible states to describe a
  greater array of errors.
  
Memory:
  This represents the accessible memory of the Y86-64 emulator.
  The memory bank is a series of 8 bit integers, held in a
  list. Instructions are stored in memory directly, and values
  are stored / retrieved in reverse order due to this 
  emulator's little endian memory syntax. The memory has a 
  default set size which should accomidate most programming
  needs. While the address encoding could certainly handle
  addresses up to 8 bytes in length, python will not, and
  should not construct a list that large. Pls do not do this.
  
 

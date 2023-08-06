[OS64]
heap_address	= 0x78000000
heap_size		= 0x02000000
stack_address	= 0x77800000
stack_size		= 0x00800000
image_address 	= 0x77000000
# entry_point	= 0x77400000

[OS32]
heap_address	= 0x78000000
heap_size		= 0x02000000
stack_address	= 0x77800000
stack_size		= 0x00800000
image_address 	= 0x77000000
# entry_point	= 0x77400000

[SMRAM]
heap_address	= 0x7A000000
heap_size		= 0x02000000
# stack_address	= 0x77800000
# stack_size	= 0x00800000
# image_address = 0x77000000

[HOB_LIST]
# EFI_GLOBAL_VARIABLE
Guid = 7739f24c-93d7-11d4-9a3a-0090273fc14d
Table = 0x00000000ffffffff

[DXE_SERVICE_TABLE]
Guid = 05ad34ba-6f02-4214-952e-4da0398e2bb9
Table = 0x00000000ffffffff

[LOADED_IMAGE_PROTOCOL]
guid = 5b1b31a1-9562-11d2-8e3f-00a0c969723b
revision = 0x1000

[MMIO]
sbreg_base = 0xFD000000
sbreg_size = 0x01000000

[LOG]
# log directory output
# usage: dir = qlog
dir =
# split log file, use with multithread
split = False


[MISC]
# append string into different logs
# maily for multiple times Ql run with one file
# usage: append = test1
append =
current_path = /
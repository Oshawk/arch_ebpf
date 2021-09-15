# Adapted from https://github.com/solana-labs/rbpf/blob/main/src/ebpf.rs

from struct import unpack

PROG_MAX_INSNS = 65536
INSN_SIZE = 8
STACK_REG = 10
FIRST_SCRATCH_REG = 6
SCRATCH_REGS = 4
ELF_INSN_DUMP_OFFSET = 29
HOST_ALIGN = 16
VIRTUAL_ADDRESS_BITS = 32

MM_PROGRAM_START = 0x100000000
MM_STACK_START = 0x200000000
MM_HEAP_START = 0x300000000
MM_INPUT_START = 0x400000000

BPF_LD = 0x00
BPF_LDX = 0x01
BPF_ST = 0x02
BPF_STX = 0x03
BPF_ALU = 0x04
BPF_JMP = 0x05
BPF_ALU64 = 0x07

BPF_W = 0x00
BPF_H = 0x08
BPF_B = 0x10
BPF_DW = 0x18

BPF_IMM = 0x00
BPF_ABS = 0x20
BPF_IND = 0x40
BPF_MEM = 0x60
BPF_XADD = 0xc0

BPF_K = 0x00
BPF_X = 0x08

BPF_ADD = 0x00
BPF_SUB = 0x10
BPF_MUL = 0x20
BPF_DIV = 0x30
BPF_OR = 0x40
BPF_AND = 0x50
BPF_LSH = 0x60
BPF_RSH = 0x70
BPF_NEG = 0x80
BPF_MOD = 0x90
BPF_XOR = 0xa0
BPF_MOV = 0xb0
BPF_ARSH = 0xc0
BPF_END = 0xd0

BPF_JA = 0x00
BPF_JEQ = 0x10
BPF_JGT = 0x20
BPF_JGE = 0x30
BPF_JSET = 0x40
BPF_JNE = 0x50
BPF_JSGT = 0x60
BPF_JSGE = 0x70
BPF_CALL = 0x80
BPF_EXIT = 0x90
BPF_JLT = 0xa0
BPF_JLE = 0xb0
BPF_JSLT = 0xc0
BPF_JSLE = 0xd0

LD_ABS_B = BPF_LD | BPF_ABS | BPF_B
LD_ABS_H = BPF_LD | BPF_ABS | BPF_H
LD_ABS_W = BPF_LD | BPF_ABS | BPF_W
LD_ABS_DW = BPF_LD | BPF_ABS | BPF_DW
LD_IND_B = BPF_LD | BPF_IND | BPF_B
LD_IND_H = BPF_LD | BPF_IND | BPF_H
LD_IND_W = BPF_LD | BPF_IND | BPF_W
LD_IND_DW = BPF_LD | BPF_IND | BPF_DW

LD_DW_IMM = BPF_LD | BPF_IMM | BPF_DW
LD_B_REG = BPF_LDX | BPF_MEM | BPF_B
LD_H_REG = BPF_LDX | BPF_MEM | BPF_H
LD_W_REG = BPF_LDX | BPF_MEM | BPF_W
LD_DW_REG = BPF_LDX | BPF_MEM | BPF_DW
ST_B_IMM = BPF_ST | BPF_MEM | BPF_B
ST_H_IMM = BPF_ST | BPF_MEM | BPF_H
ST_W_IMM = BPF_ST | BPF_MEM | BPF_W
ST_DW_IMM = BPF_ST | BPF_MEM | BPF_DW
ST_B_REG = BPF_STX | BPF_MEM | BPF_B
ST_H_REG = BPF_STX | BPF_MEM | BPF_H
ST_W_REG = BPF_STX | BPF_MEM | BPF_W
ST_DW_REG = BPF_STX | BPF_MEM | BPF_DW

ST_W_XADD = BPF_STX | BPF_XADD | BPF_W
ST_DW_XADD = BPF_STX | BPF_XADD | BPF_DW

ADD32_IMM = BPF_ALU | BPF_K | BPF_ADD
ADD32_REG = BPF_ALU | BPF_X | BPF_ADD
SUB32_IMM = BPF_ALU | BPF_K | BPF_SUB
SUB32_REG = BPF_ALU | BPF_X | BPF_SUB
MUL32_IMM = BPF_ALU | BPF_K | BPF_MUL
MUL32_REG = BPF_ALU | BPF_X | BPF_MUL
DIV32_IMM = BPF_ALU | BPF_K | BPF_DIV
DIV32_REG = BPF_ALU | BPF_X | BPF_DIV
OR32_IMM = BPF_ALU | BPF_K | BPF_OR
OR32_REG = BPF_ALU | BPF_X | BPF_OR
AND32_IMM = BPF_ALU | BPF_K | BPF_AND
AND32_REG = BPF_ALU | BPF_X | BPF_AND
LSH32_IMM = BPF_ALU | BPF_K | BPF_LSH
LSH32_REG = BPF_ALU | BPF_X | BPF_LSH
RSH32_IMM = BPF_ALU | BPF_K | BPF_RSH
RSH32_REG = BPF_ALU | BPF_X | BPF_RSH
NEG32 = BPF_ALU | BPF_NEG
MOD32_IMM = BPF_ALU | BPF_K | BPF_MOD
MOD32_REG = BPF_ALU | BPF_X | BPF_MOD
XOR32_IMM = BPF_ALU | BPF_K | BPF_XOR
XOR32_REG = BPF_ALU | BPF_X | BPF_XOR
MOV32_IMM = BPF_ALU | BPF_K | BPF_MOV
MOV32_REG = BPF_ALU | BPF_X | BPF_MOV
ARSH32_IMM = BPF_ALU | BPF_K | BPF_ARSH
ARSH32_REG = BPF_ALU | BPF_X | BPF_ARSH

LE = BPF_ALU | BPF_K | BPF_END
BE = BPF_ALU | BPF_X | BPF_END

ADD64_IMM = BPF_ALU64 | BPF_K | BPF_ADD
ADD64_REG = BPF_ALU64 | BPF_X | BPF_ADD
SUB64_IMM = BPF_ALU64 | BPF_K | BPF_SUB
SUB64_REG = BPF_ALU64 | BPF_X | BPF_SUB
MUL64_IMM = BPF_ALU64 | BPF_K | BPF_MUL
MUL64_REG = BPF_ALU64 | BPF_X | BPF_MUL
DIV64_IMM = BPF_ALU64 | BPF_K | BPF_DIV
DIV64_REG = BPF_ALU64 | BPF_X | BPF_DIV
OR64_IMM = BPF_ALU64 | BPF_K | BPF_OR
OR64_REG = BPF_ALU64 | BPF_X | BPF_OR
AND64_IMM = BPF_ALU64 | BPF_K | BPF_AND
AND64_REG = BPF_ALU64 | BPF_X | BPF_AND
LSH64_IMM = BPF_ALU64 | BPF_K | BPF_LSH
LSH64_REG = BPF_ALU64 | BPF_X | BPF_LSH
RSH64_IMM = BPF_ALU64 | BPF_K | BPF_RSH
RSH64_REG = BPF_ALU64 | BPF_X | BPF_RSH
NEG64 = BPF_ALU64 | BPF_NEG
MOD64_IMM = BPF_ALU64 | BPF_K | BPF_MOD
MOD64_REG = BPF_ALU64 | BPF_X | BPF_MOD
XOR64_IMM = BPF_ALU64 | BPF_K | BPF_XOR
XOR64_REG = BPF_ALU64 | BPF_X | BPF_XOR
MOV64_IMM = BPF_ALU64 | BPF_K | BPF_MOV
MOV64_REG = BPF_ALU64 | BPF_X | BPF_MOV
ARSH64_IMM = BPF_ALU64 | BPF_K | BPF_ARSH
ARSH64_REG = BPF_ALU64 | BPF_X | BPF_ARSH

JA = BPF_JMP | BPF_JA
JEQ_IMM = BPF_JMP | BPF_K | BPF_JEQ
JEQ_REG = BPF_JMP | BPF_X | BPF_JEQ
JGT_IMM = BPF_JMP | BPF_K | BPF_JGT
JGT_REG = BPF_JMP | BPF_X | BPF_JGT
JGE_IMM = BPF_JMP | BPF_K | BPF_JGE
JGE_REG = BPF_JMP | BPF_X | BPF_JGE
JLT_IMM = BPF_JMP | BPF_K | BPF_JLT
JLT_REG = BPF_JMP | BPF_X | BPF_JLT
JLE_IMM = BPF_JMP | BPF_K | BPF_JLE
JLE_REG = BPF_JMP | BPF_X | BPF_JLE
JSET_IMM = BPF_JMP | BPF_K | BPF_JSET
JSET_REG = BPF_JMP | BPF_X | BPF_JSET
JNE_IMM = BPF_JMP | BPF_K | BPF_JNE
JNE_REG = BPF_JMP | BPF_X | BPF_JNE
JSGT_IMM = BPF_JMP | BPF_K | BPF_JSGT
JSGT_REG = BPF_JMP | BPF_X | BPF_JSGT
JSGE_IMM = BPF_JMP | BPF_K | BPF_JSGE
JSGE_REG = BPF_JMP | BPF_X | BPF_JSGE
JSLT_IMM = BPF_JMP | BPF_K | BPF_JSLT
JSLT_REG = BPF_JMP | BPF_X | BPF_JSLT
JSLE_IMM = BPF_JMP | BPF_K | BPF_JSLE
JSLE_REG = BPF_JMP | BPF_X | BPF_JSLE

CALL_IMM = BPF_JMP | BPF_CALL
CALL_REG = BPF_JMP | BPF_X | BPF_CALL
EXIT = BPF_JMP | BPF_EXIT

BPF_CLS_MASK = 0x07
BPF_ALU_OP_MASK = 0xf0


# TODO: Make it easier to treat things as signed / unsigned. Maybe do x_u8 / x_i8 or something.
class EBPFInstruction:
    def __init__(self, ptr, data):
        self.ptr = ptr
        self.opc, src_dst, self.off, self.imm = unpack("<BBhi", data)
        self.src = src_dst >> 4
        self.dst = src_dst & 0x0f


def get_memory_address(insn):
    return insn.ptr + (insn.off + 1) * INSN_SIZE
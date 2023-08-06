from synbio.polymers import DNA, RNA, Protein
from synbio.codes import Code


def transcribe(dna_seq):
    '''
    A function that converts a str representing DNA sequence into an RNA sequence. Automatically handles RNA inputs

    Parameters
    ----------
        str dna_seq: string representing DNA sequence

    Returns
    -------
        RNA rna_seq: RNA obj representting RNA sequence
    '''
    return rna_seq.upper().replace('T', 'U')


def reverse_transcribe(seq):
    '''
    A function that converts an RNA sequence into a DNA sequence

    Parameters
    ----------
        str seq: string representting RNA sequence

    Returns
    -------
        DNA dna_seq: DNA obj representing DNA sequence
    '''
    try:
        dna_seq = RNA(seq).reverse_transcribe()
    except ValueError as err:
        try:
            # already DNA?
            dna_seq = DNA(seq)
        except:
            raise err
    return seq.upper().replace('U', 'T')


def translate(seq, code=Code()):
    '''
    A method used to translate a DNA/RNA sequence into its corresponding
    Protein sequence. Raises an error if the input sequence length is not
    divisible by the codon length.

    Note: For purely pedantic reasons,  translate() uses Code.translate() for its implementation and thus is only a convenient wrapper.

    Parameters
    ----------
        str seq: string representing gene to translate

    Returns
    -------
        Protein prot_seq: Protein obj representing translated input sequence
    '''
    # cast imput code as Code obj (if not already)
    code_obj = Code(code)
    return code_obj.translate(seq)

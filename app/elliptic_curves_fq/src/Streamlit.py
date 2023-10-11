import streamlit as st
import math
import random
import streamlit.components.v1 as components
from .Menezes_vanstone_Ascii import text_to_ascii, Menezes_Vanstone_decrybtion, Menezes_Vanstone_encrybtion, ascii_to_text
from .Kurven import Ascii
import numpy as np



def main():

    # title
    st.set_page_config(page_title="Menezes Vanstone Cryptosystem on the Field F(p^n)", layout="wide")
    
    # Side title in the main field
    st.title('Example to test Menezes Vanstone kryptosystem')
    Elliptische_Kurve  = st.sidebar.container()
    Kurve = Ascii()
    startpoint = Kurve.startpoint
    with Elliptische_Kurve:
        st.title("Elliptic Curve with following parameters")
        st.latex('y^2 = x^3 + ax + b', help=None)
        st.write(f'''a = {Kurve.a.value}, b = {Kurve.b.value}''')
        st.write("Point P = ", str(startpoint))
        st.write(f'''prime = 131, irreductible Polynome = {Kurve.a.ir_poly}''')
    
    text = st.text_input("Text to encrypt: ")
    packets = 1 + math.ceil(len(text)/16)
    if st.button('Start calculations'):
    # Create three columns layout
    
        privatekeya = random.randrange(int(Kurve.bound()[0]))
        publickey_Qa = startpoint * privatekeya

        # Create boxes for Public and Private Keys in the sidebar
        private_key_box = st.sidebar.container()
        public_key_box = st.sidebar.container()
        
        with private_key_box:
            st.title("Private key receiver: ")
            st.latex(r" \text{Privatekey } k_A: " )
            st.latex(str(privatekeya))

        with public_key_box:
            st.title("Public key receiver: ")
            st.latex(r" \text{Publickey }  Q_A = P \cdot k_A:"  )
            st.write(f" {str(publickey_Qa)} ")

        List_of_tabs= ["Scheme of en/decryption", "Total blocks", "Block 0 with lenght of message"]
        for j in range(1,packets):
            List_of_tabs.append(f"Block {j}")
        tabs = st.tabs(List_of_tabs)

        with tabs[0]:
            first_layer = st.container()
            with first_layer:
                st.subheader("Set up ")
                st.write("""Elliptic curve with equation and parameters as in the left sidebar. Point G on this Curve is given too. 
                         We construct the finite field F(131^8). The irreductible polynome is given for computation.  """)
                st.write("-----")
                st.latex(r'''\text{Receiver generates private key } k_A \text{ with integer between 0 and } q = 131^8 = 86’730’203’469’006’241''')
                st.latex(r'''\text{Receiver calculates public key Point } Q_A = P \cdot k_A \text{ |(Point addition)}''')
                st.write("-----")
                st.write("Now for every block of 2 times 8 characters in ASCII, the same scheme aplies.")
                st.write("-----")
            transform_message = st.container()
            with transform_message:
                st.subheader("Transform message in suitible form")
                st.latex(r'''\text{The sender splits the message in chunks of 2 times 8 characters. The first block is the lenght of the message in decimal digits. The next blocks are the message.}  ''')
                st.latex(r''' \text{If there are not 16 characters in the last block, then this get filled up with "-". The Sender transforms these 2 times 8 blocks in elements of } F(131^8) ''')
                st.latex(r'''\text{ Each character gets transformed in it's ASCII code and 8 form one element. Two elements form one pair} (m_{i1},m_{i2}) \text{, here named blocks.}''')
                st.write("-----")
            encryption = st.container()
            with encryption:
                st.subheader("Encryption")
                st.latex(r'''\text{Sender generates for each block private key } z_i \text{ with integer between 0 and } q = 131^8 = 86’730’203’469’006’241''')
                st.latex(r'''\text{Sender calculates Point } R_i = P \cdot z_i \text{ |(Point addition)}''')
                st.latex(r'''\text{Sender calculates Point } Q_A \cdot z_i = P \cdot k_A \cdot z_i = (s_{i1},s_{i2}) \text{ |(Point addition)}''')
                st.latex(r'''\text{Sender encrypts messagepair} (t_{i1},t_{i2}) = (m_{i1} \cdot s_{i1}, m_{i2} \cdot s_{i2}) \text{ |(multiplication in } F(131^8) \text{ (is not a point)})''')
                st.write("-----")
            exchange = st.container()
            with exchange:
                st.subheader("Exchange")
                st.latex(r''' \text{The encrypted message for each block is }(R,(t_{i1},t_{i2}))''')
                st.write("-----")
            decryption = st.container()
            with decryption:
                st.subheader("Decryption")
                st.latex(r''' \text{Receiver receives }(R,(t_{i1},t_{i2}))''')
                st.latex(r'''\text{Receiver calculates Point } R_i \cdot k_A = P  \cdot z_i \cdot k_A = P \cdot k_A \cdot z_i = (s_{i1},s_{i2}) \text{ |(Point addition)}''')
                st.latex(r'''\text{Receiver decrypts messagepair } (m_{i1},m_{i2}) = (\frac{t_{i1}}{s_{i1}}, \frac{t_{i2}}{s_{i2}}) \text{ |(division in } F(131^8) \text{ (is not a point)})''')
                st.latex(r'''\text{Receiver transforms blocks in matching ASCII symbols} ''')
                st.latex(r'''\text{Receiver merges these blocks to a string. Cuts the first block and takes so many characters as written in the first block}''')
                st.write("-----")

        with tabs[1]:
            col1, col2, col3 = st.columns([10,13,13])

            with col1:
                st.title('sender')
                st.write(("Text: " + f"**{text}**" ))
                totalmessage = (text_to_ascii(text))
                message = totalmessage[0]
                for i in range (len(totalmessage[1])):
                    for j in range(2):
                        totalmessage[1][i][j] = list(totalmessage[1][i][j])
                
                st.write(np.array(totalmessage[1]))
                st.write("---")
                st.write(np.array(message))
                
            with col2:
                st.title("exchange")        
                encrypted_with_keys = Menezes_Vanstone_encrybtion(message, Kurve, publickey_Qa)
                encrypted = encrypted_with_keys[0]
                st.write("Encrypted:")
                st.write(encrypted)

            with col3:
                st.title('receiver')
                if 'encrypted' in locals():  # Check if 'encrypted' variable exists
                    decrypted = Menezes_Vanstone_decrybtion(encrypted, Kurve, privatekeya)
                    text_decrypted = ascii_to_text(decrypted)

                    st.write("Decrypted:")
                    st.write(decrypted)
                    st.write(("Text: " + f"**{text_decrypted}**" ))
        for i in range(0, packets):
            with tabs[i+2]:
                encryption = st.container()
                with encryption:
                    st.subheader("Encryption")
                    if i == 0:
                        st.write("Lenght of message:", str(len(text)))
                    else:
                        st.write(f"**Text : {text[(i-1)*16:i*16]}**" )
                    row1, row2 = st.columns([10,10])
                    with row1:
                        st.write("Text as blocks: ", np.array(totalmessage[1][i]))
                    with row2:
                        st.write("Tranformed in ASCII: ", np.array(totalmessage[0][i]))
                    m1, m2 = totalmessage[0][i][0], totalmessage[0][i][1]
                    st.write(f"m_1 = " + str(m1) )
                    st.write(f"m_2 = " + str(m2) )
                    st.write("-----")
                    st.write(f'''Generate private key **z_{i}** = **{encrypted_with_keys[1][i]}**''')
                    st.write(f"Calculate **R** = P * z_{i} = {startpoint} * {encrypted_with_keys[1][i]} = **{encrypted[i][0]}**")
                    s = publickey_Qa * encrypted_with_keys[1][i]
                    st.write(f"Calculate **(s_1, s_2)** = Q_A * z_{i} = {publickey_Qa} * {encrypted_with_keys[1][i]} * = **{s}**")
                    st.write(f"Calculate encrypted message **t_1** = m_1 * s_1 = {m1} * {s.x.value} = **{encrypted[i][1][0].value}** ")
                    st.write(f"Calculate encrypted message **t_2** = m_2 * s_2 = {m2} * {s.y.value} = **{encrypted[i][1][1].value}** ")

                    st.write("-----")
                    
                exchange = st.container()
                with exchange:
                    st.subheader("Exchange")
                    st.write(f'''The encrypted message for this is (R,(t_1,t_2)) = ({encrypted[i][0]}, {encrypted[i][1][0].value},{encrypted[i][1][1].value})''')
                    st.write("-----")
                decryption = st.container()
                with decryption:
                    st.subheader("Decryption")
                    st.write(f"Calculate **(s_1, s_2)** = R_i * K_A = {encrypted[i][0]} * {privatekeya} * = **{s}**")
                    st.write(f"Calculate decrypted message **m_1** = t_1 / s_1 = {encrypted[i][1][0].value} / {s.x.value} = **{decrypted[2*i].value}** ")
                    st.write(f"Calculate decrypted message **m_2** = t_2 / s_2 = {encrypted[i][1][1].value} / {s.y.value} = **{decrypted[2*i+1].value}** ")
                    message1 = ""
                    for j in decrypted[2*i].value:
                        message1 += chr(j)
                    message2 = ""
                    for j in decrypted[2*i+1].value:
                        message2 += chr(j)
                    st.write("m_1 merged: " + message1)
                    st.write("m_2 merged: " + message2)

                    
                
if __name__ == '__main__':
    
    main()

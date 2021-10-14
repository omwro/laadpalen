import streamlit as st
import streamlit_lp as lp
import streamlit_ocm as ocm
import streamlit_rdw as rdw

st.title("Laadpalen case")
st.caption("Klas 3 - Groep 15 - Leden: Nassim, Omer, Max, Emmelotte")

st.markdown("## Open Charge Map")
ocm.main()

st.markdown("## Laadpalen")
lp.main()

st.markdown("## RDW")
rdw.main()

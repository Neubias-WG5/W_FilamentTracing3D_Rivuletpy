FROM python:3.6

# --------------------------------------------------------------------------------------------
# Install Cytomine python client
RUN git clone https://github.com/cytomine-uliege/Cytomine-python-client.git
RUN cd /Cytomine-python-client && git checkout tags/v2.2.0 && pip install .
RUN rm -r /Cytomine-python-client

# --------------------------------------------------------------------------------------------
# Install Neubias-W5-Utilities (annotation exporter, compute metrics, helpers,...)
RUN git clone https://github.com/Neubias-WG5/neubiaswg5-utilities.git
RUN cd /neubiaswg5-utilities/ && git checkout tags/v0.6.3 && pip install .

# Metric for TreTrc is DIADEM.jar so it needs java
# Install Java
RUN apt-get update && apt-get install openjdk-8-jdk -y && apt-get clean

# Get DiademMetric.jar and JSAP-2.1.jar files to compute DIADEM metric
RUN chmod +x /neubiaswg5-utilities/bin/*
RUN cp /neubiaswg5-utilities/bin/* /usr/bin/
# RUN cp /neubiaswg5-utilities/bin/DiademMetric.jar /usr/bin/ && cp /neubiaswg5-utilities/bin/JSAP-2.1.jar /usr/bin/ 
RUN rm -r /neubiaswg5-utilities

# --------------------------------------------------------------------------------------------
# Install needed packages to run rivuletpy as per https://github.com/RivuletStudio/rivuletpy
RUN pip install matplotlib cython tqdm libtiff scikit-fmm simpleITK bitarray
RUN pip install git+https://github.com/pearu/pylibtiff.git
RUN git clone https://github.com/RivuletStudio/rivuletpy.git
RUN cd rivuletpy && python setup.py install && pip install .
# --------------------------------------------------------------------------------------------
# Install scripts and models
ADD descriptor.json /app/descriptor.json
ADD wrapper.py /app/wrapper.py
ADD script.py /app/script.py
ADD swc_to_tiff_stack.py /app/swc_to_tiff_stack.py 

ENTRYPOINT ["python", "/app/wrapper.py"]
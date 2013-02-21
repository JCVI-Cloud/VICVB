Submit-block ::= {
  contact {
    contact {
      name
        name {
          last "__JCVI_VP_LAST_NAME__" ,
          first "__JCVI_VP_FIRST_NAME__" ,
          initials "" } ,
      affil
        std {
          affil "__JCVI_VP_INST__" ,
          div "__JCVI_VP_DEPT__" ,
          city "__JCVI_VP_CITY__" ,
          sub "__JCVI_VP__STATE__" ,
          country "__JCVI_VP_COUNTRY__" ,
          street "__JCVI_VP_STREET__" ,
          email "__JCVI_VP_EMAIL__" ,
          fax "__JCVI_VP_FAX__" ,
          phone "__JCVI_VP_PHONE__" ,
          postal-code "__JCVI_VP_ZIP__" } } } ,
  cit {
    authors {
      names
        std {
          {
            name
              name {
                last "__JCVI_VP_LAST_NAME__" ,
                first "__JCVI_VP_FIRST_NAME__" ,
                initials "" } } } ,
      affil
        std {
          affil "__JCVI_VP_INST__" ,
          div "__JCVI_VP_DEPT__" ,
          city "__JCVI_VP_CITY__" ,
          sub "__JCVI_VP__STATE__" ,
          country "__JCVI_VP_COUNTRY__" ,
          street "__JCVI_VP_STREET__" ,
          postal-code "__JCVI_VP_ZIP__" } } ,
    date
      std {
        year 2012 ,
        month 9 ,
        day 26 } } ,
  subtype new }
Seqdesc ::= pub {
  pub {
    gen {
      cit "unpublished" ,
      authors {
        names
          std {
            {
              name
                name {
                  last "__JCVI_VP_LAST_NAME__" ,
                  first "__JCVI_VP_FIRST_NAME__" ,
                  initials "" } } } ,
        affil
          std {
            affil "__JCVI_VP_INST__" ,
            div "__JCVI_VP_DEPT__" ,
            city "__JCVI_VP_CITY__" ,
            sub "__JCVI_VP__STATE__" ,
            country "__JCVI_VP_COUNTRY__" ,
            street "__JCVI_VP_STREET__" ,
            postal-code "__JCVI_VP_ZIP__" } } ,
      title "__JCVI_VP_TITLE__" } } }

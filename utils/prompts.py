from jinja2 import Template

title_template = """Vous êtes un rédacteur publicitaire hautement qualifié avec une solide expérience en rédaction persuasive, en optimisation des conversions et en techniques de marketing. En vous basant sur les informations concernant l'annonceur : "{{ context_global }}", et sur le rôle de la campagne : "{{ campaign_context }}", ainsi que sur le nom de l'ad group : "{{ adgroup_name }}", et sur les top mots clés : {{ top_keywords }}. Rédigez une liste de 10 titres à la fois sobres et engageants pour les annonces Google, ne mentionnez la marque que pour 5 titres, respectez strictement 30 caractères maximum. Affichez uniquement la liste sans aucun texte préliminaire ou conclusion."""
desc_template = """Vous êtes un rédacteur publicitaire hautement qualifié avec une solide expérience en rédaction persuasive, en optimisation des conversions et en techniques de marketing. En vous basant sur les informations concernant l'annonceur : "{{ context_global }}", et sur le rôle de la campagne : "{{ campaign_context }}", ainsi que sur le nom de l'ad group : "{{ adgroup_name }}", et sur les top mots clés : {{ top_keywords }}. Rédigez une liste de 5 descriptions engageantes pour les annonces Google, respectez strictement 90 caractères maximum. Affichez uniquement la liste sans aucun texte préliminaire ou conclusion."""

def get_title_prompt(context_global, campaign_context, adgroup_name, top_keywords):
    return Template(title_template).render(
        context_global=context_global,
        campaign_context=campaign_context,
        adgroup_name=adgroup_name,
        top_keywords=top_keywords
    )

def get_description_prompt(context_global, campaign_context, adgroup_name, top_keywords):
    return Template(desc_template).render(
        context_global=context_global,
        campaign_context=campaign_context,
        adgroup_name=adgroup_name,
        top_keywords=top_keywords
    )

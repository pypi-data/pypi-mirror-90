import cytoscape from 'https://cdnjs.cloudflare.com/ajax/libs/cytoscape/3.17.1/cytoscape.esm.min.js';
import Fuse from 'https://cdn.jsdelivr.net/npm/fuse.js@6.4.3/dist/fuse.esm.js';

class SlipboxCollection {
  constructor () {
    this.cy = cytoscape({ headless: true });
  }

  addNote (id) {
    const section = document.getElementById(id);
    const title = section.querySelector('h1').textContent;
    const filename = section.getAttribute('data-filename');
    this.cy.add({
      data: {
        id,
        title,
        filename,
        label: title,
        bgColor: 'gray'
      }
    });
  }

  addLink (source, target, tag) {
    const id = `${source}-${target}${tag}`;
    this.cy.add({ data: { id, source, target, tag } });
  }

  colorEntrypoints () {
    // Call this after inserting all notes and links.
    this.cy.nodes(e => e.indegree(false) === 0 && e.outdegree(false) > 0).data('bgColor', '#4444aa');
  }
}

function graphArea () {
  const div = document.createElement('div');
  div.innerHTML = `
    <div class="cytoscape-container" style="width: 100%; height: 80vh; padding-top: 1em; border-top: 1px solid black;"></div>
    <div class="info-container" style="bottom: 0; right: 0; padding: 20px; position: fixed; max-width: 30em; z-index: 1;">
      <header>
        <h3><a href=""></a></h3>
        <p></p>
      </header>
    </div>
  `;
  return div
}

function clusterElements (slipbox, tag) {
  const edges = slipbox.cy.edges(`[tag="${tag}"]`);
  const nodes = edges.connectedNodes();
  return nodes.union(edges.filter(e => e.data('source') !== e.data('target')))
}

function neighborElements (slipbox, id) {
  const node = slipbox.cy.getElementById(id);

  const incomingEdges = new Set();
  const incomers = node.incomers().edges('edge[tag]');
  while (incomers.length > 0) {
    const edge = incomers.pop();
    const tag = edge.data('tag');
    if (incomingEdges.has(edge)) {
      continue
    }
    incomers.push(...edge.source().incomers(`edge[tag="${tag}"]`));
    incomingEdges.add(edge);
  }

  const outgoingEdges = new Set();
  const outgoers = node.outgoers().edges('edge[tag]');
  while (outgoers.length > 0) {
    const edge = outgoers.pop();
    const tag = edge.data('tag');
    if (outgoingEdges.has(edge)) {
      continue
    }
    outgoers.push(...edge.target().outgoers(`edge[tag="${tag}"]`));
    outgoingEdges.add(edge);
  }

  const edges = slipbox.cy.collection().union(Array.from(incomingEdges)).union(Array.from(outgoingEdges));
  const nodes = edges.connectedNodes();
  const neighbors = node.openNeighborhood();
  const eles = nodes.union(edges).union(neighbors)
    .filter(e => e.isNode() || e.data('source') !== e.data('target'));

  const clone = eles.getElementById(id).clone();
  clone.data('bgColor', 'black');
  return clone.union(eles)
}

function createCytoscape (container) {
  const cy = cytoscape({
    container: container.querySelector('div.cytoscape-container'),
    selectionType: 'additive',
    style: [
      {
        selector: 'node',
        style: {
          label: 'data(label)',
          height: 'label',
          width: 'label',
          padding: '8px',
          shape: 'round-rectangle',
          color: 'white',
          'background-color': 'data(bgColor)',
          'text-halign': 'center',
          'text-valign': 'center',
          'text-wrap': 'wrap',
          'text-max-width': 100
        }
      },
      {
        selector: 'edge',
        style: {
          width: 2,
          'curve-style': 'bezier',
          'line-color': 'black',
          'line-style': 'solid',
          'target-arrow-color': 'black',
          'target-arrow-shape': 'triangle'
        }
      }
    ]
  });
  const [show, hide] = hoverHandlers(container);
  cy.on('select', 'node', show);
  cy.on('unselect', 'node', hide);
  return cy
}

function renderCytoscape (cy, layout = 'breadthfirst') {
  if (layout === 'cose') {
    cy.layout({
      name: 'cose',
      nodeDimensionsIncludeLabels: true,
      fit: true
    }).run();
  } else {
    cy.layout({
      name: 'breadthfirst',
      spacingFactor: 1.0,
      fit: true,
      directed: true,
      avoidOverlap: true,
      nodeDimensionsIncludeLabels: true
    }).run();
  }
  return cy
}

function hoverHandlers (container) {
  const infoDiv = container.querySelector('.info-container');
  const a = infoDiv.querySelector('header a');
  const p = infoDiv.querySelector('header p');

  const show = event => {
    const id = event.target.data('id');
    a.textContent = event.target.data('title');
    a.href = '#' + id;
    p.textContent = event.target.data('filename');
    event.target.data('label', id);
  };
  const hide = event => {
    a.textContent = '';
    p.textContent = '';
    event.target.data('label', event.target.data('title'));
  };
  return [show, hide]
}

function init (slipbox) {
  slipbox.colorEntrypoints();
  const extras = document.createElement('div');
  document.body.appendChild(extras);

  function resetGraph () {
    extras.style.display = 'none';
    const id = window.location.hash.slice(1);
    let elements = [];
    let layout = 'breadthfirst';
    if (!id) {
      elements = slipbox.cy.elements().filter(e => e.isNode() || e.data('source') !== e.data('target'));
      if (elements.length > 30) {
        layout = 'cose';
      }
    } else {
      const nid = Number(id);
      if (Number.isInteger(nid)) {
        elements = neighborElements(slipbox, id);
        if (elements.length < 2) return
      } else {
        elements = clusterElements(slipbox, id);
      }
    }
    if (elements.length === 0) return
    extras.style.display = 'block';
    extras.innerHTML = '';
    const container = extras.appendChild(graphArea());
    const cy = createCytoscape(container);
    cy.add(elements);
    renderCytoscape(cy, layout);
  }

  resetGraph();
  window.addEventListener('hashchange', resetGraph);
}

function init$1 () {
  const lis = document.querySelectorAll('ol.slipbox-list > li[value]');
  for (let i = 0; i < lis.length; i++) {
    const li = lis[i];
    const id = li.value;
    const section = document.querySelector(`section.slipbox-note[id="${id}"]`);
    if (!section) {
      li.remove();
      continue
    }
    const h1 = section.querySelector('h1');
    if (!h1) {
      li.remove();
      continue
    }
    const a = document.createElement('a');
    a.href = `#${id}`;
    a.innerHTML = h1.innerHTML;
    li.appendChild(a);
  }
}

function createFuse () {
  const options = {
    includeMatches: true,
    ignoreLocation: true,
    keys: ['textContent'],
    threshold: 0.45
  };
  const nodes = document.body.querySelectorAll('section.level1');
  const sections = Array.prototype.filter.call(nodes, function (node) {
    return Number.isInteger(Number(node.id))
  });
  return new Fuse(sections, options)
}

function displayResults (results, container) {
  // Display results in container.
  const div = container;
  div.textContent = '';
  for (const result of results) {
    const p = document.createElement('p');
    const heading = result.item.querySelector('h1');
    if (!heading) continue
    const title = heading.textContent;

    const h3 = document.createElement('h3');
    h3.innerHTML = `<a href="#${result.item.id}">${title}</a>`;
    p.appendChild(h3);

    let count = 3;
    for (const child of result.item.children) {
      const clone = child.cloneNode(true);
      if (count-- <= 0) break
      if (clone.tagName === 'H1' && clone.textContent === title) {
        continue
      }
      p.appendChild(clone);
    }
    div.appendChild(p);
    div.appendChild(document.createElement('hr'));
  }
}

function init$2 () {
  // Container will contain search results.
  const container = document.querySelector('#search > .search-results');
  const input = document.querySelector('nav input[type="text"]');
  input.addEventListener('change', function () {
    window.location.hash = '#search';
    const results = createFuse().search(input.value);
    displayResults(results, container);
  });
}

window.slipbox = new SlipboxCollection();

window.initSlipbox = function () {
  const title = document.getElementById('title-block-header');
  if (title) { title.remove(); }
  init$1();
  init$2();
  init(window.slipbox);
};

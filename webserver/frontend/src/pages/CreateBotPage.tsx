import { FormEvent } from 'react';
import { useNavigate } from 'react-router';
import useSWR from 'swr';
import { authenticatedFetch } from '../backend';
import Button from '../Button';
import { FormWrapper, Label } from '../Form';
import Headline from '../Headline';
import Input from '../Input';

import PageWrapper from '../PageWrapper';

export default function NewBotPage() {
  const { data: templateData } = useSWR('/api/templates');
  const navigate = useNavigate();

  if (!templateData) {
    return null;
  }

  function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const formData = new FormData(event.currentTarget);

    const body = {
      name: formData.get('name'),
      template: formData.get('template'),
    };

    authenticatedFetch('/api/repositories/', {
      method: 'POST',
      body: JSON.stringify(body),
      headers: {
        'Content-Type': 'application/json',
      },
    }).then(() => {
      navigate("/bots");
    })
  }

  return (
    <PageWrapper>
      <Headline>Create a new bot</Headline>
      <form onSubmit={onSubmit}>
        <div style={{ display: 'flex' }}>
          <FormWrapper style={{ flex: '1 1 auto', marginRight: '20px' }}>
            <Label>Name</Label>
            <Input $fullWidth name="name" required />
          </FormWrapper>
          <FormWrapper style={{ width: '30%' }}>
            <Label>Template</Label>
            <Input $fullWidth as="select" name="template" required>
              {templateData.map((item: string) => (
                <option key={item} value={item}>
                  {item}
                </option>
              ))}
            </Input>
          </FormWrapper>
        </div>
        <Button>Create</Button>
      </form>
    </PageWrapper>
  );
}
